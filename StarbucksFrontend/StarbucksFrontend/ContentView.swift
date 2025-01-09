//
//  ContentView.swift
//  StarbucksFrontend
//
//  Created by Archita Nemalikanti on 1/4/25.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        NavigationStack {
            VStack {
                // Title text
                Text("Sign-up as a...")
                    .font(.system(size: 32, weight: .medium, design: .default))
                    .foregroundColor(.black)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(.top, 92)
                    .padding(.leading, 20)
                
                // Gradient line
                LinearGradient(
                    gradient: Gradient(colors: [Color.gray.opacity(0.8), Color.gray.opacity(0.2), Color.clear]),
                    startPoint: .top,
                    endPoint: .bottom
                )
                .frame(height: 4) // Adjust thickness
                .padding(.horizontal, 20) // Align with the title
                
                Spacer()
                
                // Shift Lead button
                NavigationLink(destination: ShiftLeadView()) {
                    VStack {
                        Image("Image") // Replace with your icon
                            .resizable()
                            .frame(width: 63, height: 63)
                            .padding()
                        Text("Shift Lead")
                            .font(.title2)
                            .fontWeight(.bold) // Make the text bold
                            .foregroundColor(.black)
                    }
                    .frame(width: 120, height: 120)
                    .padding()
                    .background(RoundedRectangle(cornerRadius: 12).stroke(Color.black, lineWidth: 2))
                }
                .padding()
                
                // Barista button
                NavigationLink(destination: BaristaView()) {
                    VStack {
                        Image("StarbucksCup") // Replace with your icon
                            .resizable()
                            .frame(width: 60, height: 70)
                            .padding()
                        Text("Barista")
                            .font(.title2)
                            .fontWeight(.bold) // Make the text bold
                            .foregroundColor(.black)
                    }
                    .frame(width: 120, height: 120)
                    .padding()
                    .background(RoundedRectangle(cornerRadius: 12).stroke(Color.black, lineWidth: 2))
                }
                .padding()
                
                Spacer()
                
                // Login section
                VStack(spacing: 20) {
                    Text("Already have an account?\nLog in here!")
                        .foregroundColor(.black)
                        .multilineTextAlignment(.center)
                    
                    // Login button
                    NavigationLink(destination: LogInView()) {
                        ZStack {
                            RoundedRectangle(cornerRadius: 10)
                                .foregroundColor(.blue)
                                .frame(height: 50) // Set a height for the button

                            Text("Log In")
                                .foregroundColor(.white)
                                .bold()
                        }
                        .frame(width: 200)
                    }
                }
                .padding()
                
                Spacer()
            }
        } // End NavigationStack
    }
}

struct ShiftLeadView: View {
    
    var body: some View {
        
        VStack {
            // Centered Welcome Text
            Text("Welcome Shift Leads!")
                .font(.title) // Smaller than .largeTitle
                .fontWeight(.light) // Adjust text weight
                .multilineTextAlignment(.center) // Center text alignment
                .padding(.top, 40) // Adjust top padding if needed
            
            Form {
                TextField("Full Name", text: $name)
                    .textFieldStyle(DefaultTextFieldStyle())
                    .autocorrectionDisabled()
                
                TextField("Username", text: $username)
                    .textFieldStyle(DefaultTextFieldStyle())
                    .autocapitalization(/*@START_MENU_TOKEN@*/.none/*@END_MENU_TOKEN@*/)
                    .autocorrectionDisabled()
                
                SecureField("Password", text: $password)
                    .textFieldStyle(DefaultTextFieldStyle())
                    .autocorrectionDisabled()
                
                TextField("Starbucks Location", text: $starbucksLocation)
                    .textFieldStyle(DefaultTextFieldStyle())
                    .autocorrectionDisabled()
                
                SBButton(
                    title: "Create Account",
                    background: .green
                ) {
                    //attempt registration
                }
                .padding()
            }
            
            
            
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .top)
        Spacer() // Pushes remaining content downwards
    }
}

// Dummy BaristaView
struct BaristaView: View {
    
    @State private var name: String = ""
    @State private var email: String = ""
    @State private var password: String = ""
    @State private var username: String = ""
    @State private var starbucksLocation: String = ""
    
    var body: some View {
        VStack {
            // Centered Welcome Text
            Text("Welcome Baristas!")
                .font(.title) // Smaller than .largeTitle
                .fontWeight(.light) // Adjust text weight
                .multilineTextAlignment(.center) // Center text alignment
                .padding(.top, 40) // Adjust top padding if needed
            
            Form {
                TextField("Full Name", text: $name)
                    .textFieldStyle(DefaultTextFieldStyle())
                    .autocorrectionDisabled()
                
                TextField("Username", text: $username)
                    .textFieldStyle(DefaultTextFieldStyle())
                    .autocapitalization(/*@START_MENU_TOKEN@*/.none/*@END_MENU_TOKEN@*/)
                    .autocorrectionDisabled()
                
                SecureField("Password", text: $password)
                    .textFieldStyle(DefaultTextFieldStyle())
                    .autocorrectionDisabled()
                
                TextField("Starbucks Location", text: $starbucksLocation)
                    .textFieldStyle(DefaultTextFieldStyle())
                    .autocorrectionDisabled()
                
                SBButton(
                    title: "Create Account",
                    background: .green
                ) {
                    //attempt registration
                }
                .padding()
            }
            
            
            
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .top)
        Spacer() // Pushes remaining content downwards
    }

}

// Dummy Log In View
struct LogInView: View {
    @StateObject var viewModel = LoginViewModel()
    @State private var password = ""
    
    var body: some View {
        VStack {
            Text("Welcome Back!")
                .font(.system(size: 32))
                .fontWeight(.medium)
                .multilineTextAlignment(.center)
                .padding(.top, 139)
            
            Spacer()
            
            
            
            // Log In Form
            Form {
                
                if !viewModel.errorMessage.isEmpty {
                    Text(viewModel.errorMessage)
                        .foregroundColor(Color.red)
                    
                }
                
                TextField("Username", text: $viewModel.username)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .autocorrectionDisabled()
                
                SecureField("Password", text: $viewModel.password)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .autocorrectionDisabled()
                
                SBButton(
                    title: "Log In",
                    background: .blue
                ) {
                    viewModel.login()
                }
                .padding()
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
    }
    
    // Preview
    #Preview {
        ContentView()
    }
}
