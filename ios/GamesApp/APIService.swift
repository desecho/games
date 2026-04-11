import Combine
import Foundation

@MainActor
final class APIService: ObservableObject {
    @Published var isAuthenticated: Bool
    @Published var username: String?
    @Published var isLoading = false
    @Published var isRecordsLoading = false
    @Published var errorMessage: String?
    @Published var records: [GameRecord] = []

    private enum StorageKey {
        static let accessToken = "games_access_token"
        static let refreshToken = "games_refresh_token"
        static let username = "games_username"
    }

    private let baseURL: URL = {
        #if DEBUG
        return URL(string: "http://localhost:8000")!
        #else
        return URL(string: "https://api.games.samarchyan.me")!
        #endif
    }()

    private var accessToken: String? {
        get {
            UserDefaults.standard.string(forKey: StorageKey.accessToken)
        }
        set {
            if let newValue {
                UserDefaults.standard.set(newValue, forKey: StorageKey.accessToken)
            } else {
                UserDefaults.standard.removeObject(forKey: StorageKey.accessToken)
            }
            isAuthenticated = newValue != nil
        }
    }

    private var refreshToken: String? {
        get {
            UserDefaults.standard.string(forKey: StorageKey.refreshToken)
        }
        set {
            if let newValue {
                UserDefaults.standard.set(newValue, forKey: StorageKey.refreshToken)
            } else {
                UserDefaults.standard.removeObject(forKey: StorageKey.refreshToken)
            }
        }
    }

    init() {
        let storedToken = UserDefaults.standard.string(forKey: StorageKey.accessToken)
        isAuthenticated = storedToken != nil
        username = UserDefaults.standard.string(forKey: StorageKey.username)
    }

    func login(username: String, password: String) async {
        isLoading = true
        errorMessage = nil

        do {
            let body = LoginRequest(username: username, password: password)
            let request = try makeRequest(path: "token/", method: "POST", body: body, authenticated: false)
            let response: LoginResponse = try await send(request)
            accessToken = response.access
            refreshToken = response.refresh
            self.username = username
            UserDefaults.standard.set(username, forKey: StorageKey.username)
            errorMessage = nil
        } catch let error as APIError {
            errorMessage = "Login failed: \(error.localizedDescription)"
            isLoading = false
            return
        } catch {
            errorMessage = "Login failed: \(APIError.networkError.localizedDescription)"
            isLoading = false
            return
        }

        isLoading = false

        do {
            try await loadRecords()
        } catch {
            errorMessage = error.localizedDescription
        }
    }

    func logout() {
        accessToken = nil
        refreshToken = nil
        username = nil
        records = []
        errorMessage = nil
        UserDefaults.standard.removeObject(forKey: StorageKey.username)
    }

    func loadRecords() async throws {
        guard isAuthenticated else {
            return
        }

        isRecordsLoading = true
        defer {
            isRecordsLoading = false
        }

        do {
            let request = try makeRequest(path: "records/", authenticated: true)
            let fetchedRecords: [GameRecord] = try await send(request)
            records = fetchedRecords.sortedForDisplay()
        } catch let error as APIError {
            handleAuthenticatedError(error)
            throw error
        } catch {
            throw APIError.networkError
        }
    }

    func records(for list: GameList) -> [GameRecord] {
        records
            .filter { $0.listKey == list.key }
            .sortedForDisplay()
    }

    func searchGames(query: String) async throws -> [Game] {
        let trimmedQuery = query.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmedQuery.isEmpty else {
            return []
        }

        do {
            let request = try makeRequest(
                path: "search/",
                queryItems: [URLQueryItem(name: "query", value: trimmedQuery)],
                authenticated: isAuthenticated
            )
            let games: [Game] = try await send(request)
            return games.sorted { $0.name.localizedCaseInsensitiveCompare($1.name) == .orderedAscending }
        } catch let error as APIError {
            if isAuthenticated {
                handleAuthenticatedError(error)
            }
            throw error
        } catch {
            throw APIError.networkError
        }
    }

    func addGame(gameId: Int, to list: GameList) async throws {
        let body = AddRecordRequest(listId: list.id, gameId: gameId)
        do {
            let request = try makeRequest(path: "records/add/", method: "POST", body: body, authenticated: true)
            try await sendVoid(request)
            try await loadRecords()
        } catch let error as APIError {
            handleAuthenticatedError(error)
            throw error
        } catch {
            throw APIError.networkError
        }
    }

    func moveRecord(_ record: GameRecord, to list: GameList) async throws {
        let body = ChangeListRequest(listId: list.id)
        do {
            let request = try makeRequest(
                path: "records/\(record.id)/change-list/",
                method: "PUT",
                body: body,
                authenticated: true
            )
            try await sendVoid(request)
            try await loadRecords()
        } catch let error as APIError {
            handleAuthenticatedError(error)
            throw error
        } catch {
            throw APIError.networkError
        }
    }

    func deleteRecord(_ record: GameRecord) async throws {
        do {
            let request = try makeRequest(path: "records/\(record.id)/delete/", method: "DELETE", authenticated: true)
            try await sendVoid(request)
            try await loadRecords()
        } catch let error as APIError {
            handleAuthenticatedError(error)
            throw error
        } catch {
            throw APIError.networkError
        }
    }

    func updateRating(record: GameRecord, rating: Int) async throws {
        guard (0...5).contains(rating) else {
            return
        }

        let body = RatingRequest(rating: rating)
        do {
            let request = try makeRequest(
                path: "records/\(record.id)/rating/",
                method: "PUT",
                body: body,
                authenticated: true
            )
            try await sendVoid(request)
            updateCachedRating(recordID: record.id, rating: rating)
        } catch let error as APIError {
            handleAuthenticatedError(error)
            throw error
        } catch {
            throw APIError.networkError
        }
    }

    private func updateCachedRating(recordID: Int, rating: Int) {
        records = records.map { record in
            guard record.id == recordID else {
                return record
            }
            return GameRecord(
                id: record.id,
                game: record.game,
                listKey: record.listKey,
                order: record.order,
                rating: rating
            )
        }
    }

    private func makeRequest(
        path: String,
        method: String = "GET",
        body: (some Encodable)? = Optional<String>.none,
        queryItems: [URLQueryItem] = [],
        authenticated: Bool
    ) throws -> URLRequest {
        var base = baseURL.absoluteString
        if !base.hasSuffix("/") {
            base += "/"
        }

        let normalizedPath = path.hasPrefix("/") ? String(path.dropFirst()) : path
        guard var components = URLComponents(string: base + normalizedPath) else {
            throw APIError.invalidURL
        }

        if !queryItems.isEmpty {
            components.queryItems = queryItems
        }

        guard let url = components.url else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json; charset=UTF-8", forHTTPHeaderField: "Content-Type")
        request.setValue("XMLHttpRequest", forHTTPHeaderField: "X-Requested-With")

        if authenticated {
            guard let accessToken else {
                throw APIError.missingToken
            }
            request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")
        }

        if let body {
            request.httpBody = try JSONEncoder().encode(body)
        }

        return request
    }

    private func send<T: Decodable>(_ request: URLRequest) async throws -> T {
        let data = try await sendData(request)
        do {
            return try JSONDecoder().decode(T.self, from: data)
        } catch {
            throw APIError.decodingError
        }
    }

    private func sendVoid(_ request: URLRequest) async throws {
        _ = try await sendData(request)
    }

    private func sendData(_ request: URLRequest) async throws -> Data {
        do {
            let (data, response) = try await URLSession.shared.data(for: request)
            guard let httpResponse = response as? HTTPURLResponse else {
                throw APIError.networkError
            }

            switch httpResponse.statusCode {
            case 200...299:
                return data
            case 401:
                throw APIError.unauthorized(errorMessage(from: data))
            case 403:
                throw APIError.forbidden(errorMessage(from: data))
            case 404:
                throw APIError.notFound(errorMessage(from: data))
            case 500...599:
                throw APIError.serverError(errorMessage(from: data))
            default:
                throw APIError.unknown(httpResponse.statusCode, errorMessage(from: data))
            }
        } catch let error as APIError {
            throw error
        } catch {
            throw APIError.networkError
        }
    }

    private func errorMessage(from data: Data) -> String? {
        guard !data.isEmpty else {
            return nil
        }
        return try? JSONDecoder().decode(APIErrorBody.self, from: data).message
    }

    private func handleAuthenticatedError(_ error: APIError) {
        if case .unauthorized = error {
            logout()
            errorMessage = error.localizedDescription
        }
    }
}

private extension Array where Element == GameRecord {
    func sortedForDisplay() -> [GameRecord] {
        sorted { left, right in
            if left.order != right.order {
                return left.order < right.order
            }
            return left.game.name.localizedCaseInsensitiveCompare(right.game.name) == .orderedAscending
        }
    }
}
