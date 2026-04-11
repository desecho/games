import SwiftUI

struct SearchView: View {
    @EnvironmentObject private var apiService: APIService

    @State private var query = ""
    @State private var results: [Game] = []
    @State private var isSearching = false
    @State private var isAddingGameID: Int?
    @State private var hasSearched = false
    @State private var errorMessage: String?

    private var canSearch: Bool {
        !query.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty && !isSearching
    }

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                searchBar
                    .padding()

                Group {
                    if isSearching {
                        ProgressView("Searching games...")
                            .frame(maxWidth: .infinity, maxHeight: .infinity)
                    } else if results.isEmpty && hasSearched {
                        ContentUnavailableView(
                            "No Results",
                            systemImage: "magnifyingglass",
                            description: Text("Try a different game title.")
                        )
                    } else if results.isEmpty {
                        ContentUnavailableView(
                            "Search Games",
                            systemImage: "gamecontroller",
                            description: Text("Find games to add to your lists.")
                        )
                    } else {
                        List {
                            ForEach(results) { game in
                                SearchResultRow(
                                    game: game,
                                    isAdding: isAddingGameID == game.id,
                                    addAction: { list in
                                        add(game, to: list)
                                    }
                                )
                            }
                        }
                        .listStyle(.plain)
                    }
                }
            }
            .navigationTitle("Search")
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button("Logout") {
                        apiService.logout()
                    }
                }
            }
            .alert("Error", isPresented: Binding(
                get: { errorMessage != nil },
                set: { visible in
                    if !visible {
                        errorMessage = nil
                    }
                }
            )) {
                Button("OK", role: .cancel) {
                    errorMessage = nil
                }
            } message: {
                Text(errorMessage ?? "")
            }
        }
    }

    private var searchBar: some View {
        HStack(spacing: 10) {
            TextField("Search", text: $query)
                .textInputAutocapitalization(.never)
                .autocorrectionDisabled()
                .textFieldStyle(.roundedBorder)
                .submitLabel(.search)
                .onSubmit {
                    search()
                }

            Button("Search") {
                search()
            }
            .buttonStyle(.borderedProminent)
            .disabled(!canSearch)
        }
    }

    private func search() {
        guard canSearch else {
            return
        }

        isSearching = true
        hasSearched = true
        errorMessage = nil

        Task {
            do {
                results = try await apiService.searchGames(query: query)
            } catch {
                errorMessage = error.localizedDescription
            }
            isSearching = false
        }
    }

    private func add(_ game: Game, to list: GameList) {
        guard isAddingGameID == nil else {
            return
        }

        isAddingGameID = game.id
        Task {
            do {
                try await apiService.addGame(gameId: game.id, to: list)
                results.removeAll { $0.id == game.id }
            } catch {
                errorMessage = error.localizedDescription
            }
            isAddingGameID = nil
        }
    }
}

private struct SearchResultRow: View {
    let game: Game
    let isAdding: Bool
    let addAction: (GameList) -> Void

    private var availableLists: [GameList] {
        GameList.allCases.filter { $0.canAccept(game) }
    }

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            GameCoverView(game: game)

            VStack(alignment: .leading, spacing: 6) {
                Text(game.name)
                    .font(.headline)
                    .lineLimit(2)

                Text(game.category)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)

                if !game.isReleased {
                    Label("Unreleased", systemImage: "clock")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }

                Menu {
                    ForEach(availableLists) { list in
                        Button {
                            addAction(list)
                        } label: {
                            Label(list.title, systemImage: list.systemImage)
                        }
                    }
                } label: {
                    if isAdding {
                        Label("Adding", systemImage: "hourglass")
                    } else {
                        Label("Add", systemImage: "plus")
                    }
                }
                .font(.subheadline)
                .disabled(isAdding)
            }

            if isAdding {
                Spacer()
                ProgressView()
            }
        }
        .padding(.vertical, 6)
    }
}
