import Foundation

struct LoginRequest: Encodable {
    let username: String
    let password: String
}

struct LoginResponse: Decodable {
    let access: String
    let refresh: String
}

struct EmptyResponse: Decodable {}

struct APIErrorBody: Decodable {
    let detail: String?
    let error: String?
    let nonFieldErrors: [String]?

    enum CodingKeys: String, CodingKey {
        case detail
        case error
        case nonFieldErrors = "non_field_errors"
    }

    var message: String? {
        if let detail, !detail.isEmpty {
            return detail
        }
        if let error, !error.isEmpty {
            return error
        }
        if let nonFieldErrors, !nonFieldErrors.isEmpty {
            return nonFieldErrors.joined(separator: " ")
        }
        return nil
    }
}

enum APIError: LocalizedError {
    case invalidURL
    case missingToken
    case unauthorized(String?)
    case forbidden(String?)
    case notFound(String?)
    case serverError(String?)
    case decodingError
    case networkError
    case unknown(Int, String?)

    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid backend URL."
        case .missingToken:
            return "Please log in again."
        case .unauthorized(let message):
            return message ?? "Your session has expired. Please log in again."
        case .forbidden(let message):
            return message ?? "You do not have permission to access this resource."
        case .notFound(let message):
            return message ?? "The requested resource was not found."
        case .serverError(let message):
            return message ?? "Server error occurred. Please try again later."
        case .decodingError:
            return "Failed to process the server response."
        case .networkError:
            return "Network connection error. Please check your connection."
        case .unknown(let statusCode, let message):
            return message ?? "An error occurred. Status: \(statusCode)."
        }
    }
}

enum ListKey: String, Codable, CaseIterable {
    case wantToPlay = "want-to-play"
    case playing
    case beaten
    case onHold = "on-hold"
}

enum GameList: Int, CaseIterable, Identifiable {
    case wantToPlay = 1
    case playing
    case beaten
    case onHold

    var id: Int {
        rawValue
    }

    var key: ListKey {
        switch self {
        case .wantToPlay:
            return .wantToPlay
        case .playing:
            return .playing
        case .beaten:
            return .beaten
        case .onHold:
            return .onHold
        }
    }

    var title: String {
        switch self {
        case .wantToPlay:
            return "Want to Play"
        case .playing:
            return "Playing"
        case .beaten:
            return "Beaten"
        case .onHold:
            return "On Hold"
        }
    }

    var systemImage: String {
        switch self {
        case .wantToPlay:
            return "star"
        case .playing:
            return "gamecontroller"
        case .beaten:
            return "trophy"
        case .onHold:
            return "pause.circle"
        }
    }

    func canAccept(_ game: Game) -> Bool {
        self == .wantToPlay || game.isReleased
    }
}

struct Game: Codable, Identifiable, Equatable {
    let id: Int
    let name: String
    let cover: String?
    let category: String
    let isReleased: Bool

    var coverURL: URL? {
        guard let cover, !cover.isEmpty else {
            return nil
        }
        return URL(string: cover)
    }
}

struct GameRecord: Codable, Identifiable, Equatable {
    let id: Int
    let game: Game
    let listKey: ListKey
    let order: Int
    let rating: Int
}

struct AddRecordRequest: Encodable {
    let listId: Int
    let gameId: Int
}

struct ChangeListRequest: Encodable {
    let listId: Int
}

struct RatingRequest: Encodable {
    let rating: Int
}
