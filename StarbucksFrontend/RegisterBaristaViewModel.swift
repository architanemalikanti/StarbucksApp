//
//  RegisterBaristaViewModel.swift
//  StarbucksFrontend
//
//  Created by Archita Nemalikanti on 1/9/25.
//

import Foundation

//
//  RegisterShiftLeadViewModel.swift
//  StarbucksFrontend
//
//  Created by Archita Nemalikanti on 1/7/25.
//

import Foundation

class RegisterBaristaViewModel: ObservableObject {
    @Published var name: String = ""
    @Published var email: String = ""
    @Published var password: String = ""
    @Published var username: String = ""
    @Published var starbucksLocation: String = ""
    @Published var errorMessage: String = ""
    
    
    init () {}
    
    func register (){
        guard validate() else {
            errorMessage = "Please fill in all fields correctly."
            return
        }
        
        //create a user:
        // Prepare the URL for the Flask API
        guard let url = URL(string: "http://127.0.0.1:8000/registerBarista/") else {
            errorMessage = "Invalid server URL."
            return
        }
        
        // Create the payload
        let payload: [String: Any] = [
            "fullName": name,
            "userName": username,
            "password": password,
            "starbucksLocation": starbucksLocation
        ]
        
        // Convert the payload to JSON data
        guard let jsonData = try? JSONSerialization.data(withJSONObject: payload) else {
            errorMessage = "Failed to create JSON payload."
            return
        }
        
        // Create the request
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
        
        // Make the HTTP request
        URLSession.shared.dataTask(with: request) { data, response, error in
            // Handle network errors
            if let error = error {
                DispatchQueue.main.async {
                    self.errorMessage = "Request failed: \(error.localizedDescription)"
                }
                return
            }
        // Parse the response
        if let data = data, let httpResponse = response as? HTTPURLResponse {
                DispatchQueue.main.async {
                    if httpResponse.statusCode == 201 {
                        self.errorMessage = "Registration successful!"
                    } else {
                        if let message = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                           let errorMessage = message["error"] as? String {
                            self.errorMessage = errorMessage
                        } else {
                            self.errorMessage = "Something went wrong."
                        }
                    }
                }
            }
        }.resume()
        
        
    }
    
    private func validate() -> Bool {
        guard !name.trimmingCharacters(in: .whitespaces).isEmpty,
              !password.trimmingCharacters(in: .whitespaces).isEmpty,
              !username.trimmingCharacters(in: .whitespaces).isEmpty,
              !starbucksLocation.trimmingCharacters(in: .whitespaces).isEmpty else {
            return false
        }
        
        guard password.count >= 6 else {
            return false //password
        }
        return true
        
    }
    
    
    
}
