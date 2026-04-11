import SwiftUI

struct LoginView: View {
    @EnvironmentObject private var apiService: APIService
    @State private var username = ""
    @State private var password = ""

    private var canSubmit: Bool {
        !username.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty &&
            !password.isEmpty &&
            !apiService.isLoading
    }

    var body: some View {
        NavigationStack {
            VStack(spacing: 24) {
                Spacer()

                VStack(spacing: 12) {
                    Image("Logo")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 120, height: 120)
                        .clipShape(RoundedRectangle(cornerRadius: 24))
                        .accessibilityLabel("Games logo")

                    Text("Games")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                }

                VStack(spacing: 14) {
                    TextField("Username", text: $username)
                        .textContentType(.username)
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled()
                        .submitLabel(.next)
                        .padding(12)
                        .background(.thinMaterial)
                        .clipShape(RoundedRectangle(cornerRadius: 8))

                    SecureField("Password", text: $password)
                        .textContentType(.password)
                        .submitLabel(.go)
                        .onSubmit {
                            submit()
                        }
                        .padding(12)
                        .background(.thinMaterial)
                        .clipShape(RoundedRectangle(cornerRadius: 8))
                }

                if let errorMessage = apiService.errorMessage {
                    Text(errorMessage)
                        .font(.callout)
                        .foregroundStyle(.red)
                        .multilineTextAlignment(.center)
                        .frame(maxWidth: .infinity)
                }

                Button {
                    submit()
                } label: {
                    HStack {
                        if apiService.isLoading {
                            ProgressView()
                                .tint(.white)
                        }
                        Text("Login")
                            .fontWeight(.semibold)
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                }
                .buttonStyle(.borderedProminent)
                .disabled(!canSubmit)

                Spacer()
            }
            .padding(24)
        }
    }

    private func submit() {
        guard canSubmit else {
            return
        }

        let trimmedUsername = username.trimmingCharacters(in: .whitespacesAndNewlines)
        Task {
            await apiService.login(username: trimmedUsername, password: password)
        }
    }
}
