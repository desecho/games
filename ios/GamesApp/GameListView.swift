import SwiftUI

private enum GameViewMode: Equatable {
    case list
    case gallery

    var toggleSystemImage: String {
        switch self {
        case .list:
            return "square.grid.3x3"
        case .gallery:
            return "list.bullet"
        }
    }

    var toggleAccessibilityLabel: String {
        switch self {
        case .list:
            return "Show gallery view"
        case .gallery:
            return "Show list view"
        }
    }

    mutating func toggle() {
        self = self == .list ? .gallery : .list
    }
}

struct GameListView: View {
    @EnvironmentObject private var apiService: APIService
    let list: GameList

    @State private var errorMessage: String?
    @State private var currentViewMode: GameViewMode = .list

    private var records: [GameRecord] {
        apiService.records(for: list)
    }

    var body: some View {
        NavigationStack {
            Group {
                if apiService.isRecordsLoading && records.isEmpty {
                    ProgressView("Loading games...")
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else if records.isEmpty {
                    ContentUnavailableView(
                        "No Games",
                        systemImage: list.systemImage,
                        description: Text("Search for games and add them to \(list.title).")
                    )
                } else if currentViewMode == .gallery {
                    GameGalleryView(records: records)
                        .refreshable {
                            await reload()
                        }
                } else {
                    List {
                        ForEach(records) { record in
                            GameRecordRow(
                                record: record,
                                currentList: list,
                                errorMessage: $errorMessage
                            )
                        }
                    }
                    .listStyle(.plain)
                    .refreshable {
                        await reload()
                    }
                }
            }
            .navigationTitle(list.title)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button("Logout") {
                        apiService.logout()
                    }
                }

                ToolbarItemGroup(placement: .topBarTrailing) {
                    Button {
                        currentViewMode.toggle()
                    } label: {
                        Image(systemName: currentViewMode.toggleSystemImage)
                    }
                    .accessibilityLabel(currentViewMode.toggleAccessibilityLabel)

                    Button {
                        Task {
                            await reload()
                        }
                    } label: {
                        Image(systemName: "arrow.clockwise")
                    }
                    .disabled(apiService.isRecordsLoading)
                    .accessibilityLabel("Reload games")
                }
            }
            .task {
                if apiService.records.isEmpty {
                    await reload()
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

    private func reload() async {
        do {
            try await apiService.loadRecords()
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}

private struct GameGalleryView: View {
    let records: [GameRecord]

    private let columns = [
        GridItem(.adaptive(minimum: 104), spacing: 12)
    ]

    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 14) {
                ForEach(records) { record in
                    GameGalleryItemView(record: record)
                }
            }
            .padding(12)
        }
    }
}

private struct GameGalleryItemView: View {
    let record: GameRecord

    var body: some View {
        VStack(spacing: 6) {
            AsyncImage(url: record.game.coverURL) { phase in
                switch phase {
                case .success(let image):
                    image
                        .resizable()
                        .scaledToFill()
                case .failure:
                    placeholder
                case .empty:
                    ProgressView()
                @unknown default:
                    placeholder
                }
            }
            .aspectRatio(0.75, contentMode: .fit)
            .frame(maxWidth: .infinity)
            .background(Color.secondary.opacity(0.12))
            .clipShape(RoundedRectangle(cornerRadius: 8))
            .shadow(color: .black.opacity(0.08), radius: 2, x: 0, y: 1)

            Text(record.game.name)
                .font(.caption)
                .fontWeight(.medium)
                .lineLimit(2)
                .multilineTextAlignment(.center)
                .frame(maxWidth: .infinity)

            if !record.game.isReleased {
                Label("Unreleased", systemImage: "clock")
                    .font(.caption2)
                    .foregroundStyle(.secondary)
                    .lineLimit(1)
            }
        }
        .accessibilityElement(children: .combine)
    }

    private var placeholder: some View {
        Image(systemName: "gamecontroller")
            .font(.title2)
            .foregroundStyle(.secondary)
            .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

private struct GameRecordRow: View {
    @EnvironmentObject private var apiService: APIService
    let record: GameRecord
    let currentList: GameList
    @Binding var errorMessage: String?

    @State private var isMutating = false

    private var availableLists: [GameList] {
        GameList.allCases.filter { candidate in
            candidate != currentList && candidate.canAccept(record.game)
        }
    }

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            GameCoverView(game: record.game)

            VStack(alignment: .leading, spacing: 8) {
                VStack(alignment: .leading, spacing: 3) {
                    Text(record.game.name)
                        .font(.headline)
                        .lineLimit(2)

                    Text(record.game.category)
                        .font(.subheadline)
                        .foregroundStyle(.secondary)

                    if !record.game.isReleased {
                        Label("Unreleased", systemImage: "clock")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }
                }

                RatingControl(record: record, errorMessage: $errorMessage)

                HStack(spacing: 10) {
                    if !availableLists.isEmpty {
                        Menu {
                            ForEach(availableLists) { list in
                                Button {
                                    mutate {
                                        try await apiService.moveRecord(record, to: list)
                                    }
                                } label: {
                                    Label(list.title, systemImage: list.systemImage)
                                }
                            }
                        } label: {
                            Label("Move", systemImage: "arrow.right.arrow.left")
                        }
                        .disabled(isMutating)
                    }

                    Button(role: .destructive) {
                        mutate {
                            try await apiService.deleteRecord(record)
                        }
                    } label: {
                        Label("Delete", systemImage: "trash")
                    }
                    .disabled(isMutating)
                }
                .font(.subheadline)
            }

            if isMutating {
                Spacer()
                ProgressView()
            }
        }
        .padding(.vertical, 6)
    }

    private func mutate(_ operation: @escaping () async throws -> Void) {
        guard !isMutating else {
            return
        }

        isMutating = true
        Task {
            do {
                try await operation()
            } catch {
                errorMessage = error.localizedDescription
            }
            isMutating = false
        }
    }
}

private struct RatingControl: View {
    @EnvironmentObject private var apiService: APIService
    let record: GameRecord
    @Binding var errorMessage: String?

    @State private var isUpdating = false

    var body: some View {
        HStack(spacing: 3) {
            ForEach(1...5, id: \.self) { value in
                Button {
                    updateRating(value == record.rating ? 0 : value)
                } label: {
                    Image(systemName: value <= record.rating ? "star.fill" : "star")
                        .foregroundStyle(.yellow)
                }
                .buttonStyle(.plain)
                .disabled(isUpdating)
                .accessibilityLabel(value == record.rating ? "Clear rating" : "Set rating to \(value)")
            }

            if record.rating == 0 {
                Text("Unrated")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .padding(.leading, 4)
            }
        }
    }

    private func updateRating(_ rating: Int) {
        guard !isUpdating else {
            return
        }

        isUpdating = true
        Task {
            do {
                try await apiService.updateRating(record: record, rating: rating)
            } catch {
                errorMessage = error.localizedDescription
            }
            isUpdating = false
        }
    }
}

struct GameCoverView: View {
    let game: Game

    var body: some View {
        AsyncImage(url: game.coverURL) { phase in
            switch phase {
            case .success(let image):
                image
                    .resizable()
                    .scaledToFill()
            case .failure:
                placeholder
            case .empty:
                ProgressView()
            @unknown default:
                placeholder
            }
        }
        .frame(width: 72, height: 96)
        .background(Color.secondary.opacity(0.12))
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }

    private var placeholder: some View {
        Image(systemName: "gamecontroller")
            .font(.title2)
            .foregroundStyle(.secondary)
            .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
