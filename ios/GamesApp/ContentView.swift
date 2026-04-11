import SwiftUI

struct ContentView: View {
    @StateObject private var apiService = APIService()

    var body: some View {
        Group {
            if apiService.isAuthenticated {
                MainTabView()
            } else {
                LoginView()
            }
        }
        .environmentObject(apiService)
    }
}

private struct MainTabView: View {
    var body: some View {
        TabView {
            ForEach(GameList.allCases) { list in
                GameListView(list: list)
                    .tabItem {
                        Label(list.title, systemImage: list.systemImage)
                    }
            }

            SearchView()
                .tabItem {
                    Label("Search", systemImage: "magnifyingglass")
                }
        }
    }
}
