//
//  LoginViewModel.swift
//  StarbucksFrontend
//
//  Created by Archita Nemalikanti on 1/6/25.
//

import Foundation

class LoginViewModel: ObservableObject {
    
    @Published var username = ""
    @Published var password = ""
    @Published var errorMessage = ""
    
    init(){ }
    
    
    //log in the user
    func login() {
        
        //first, validate the user
        guard validate() else {
            return
        }
        
        //then, try to log the user in
        
    }
    
    //validate the email and password
    public func validate() -> Bool {
        errorMessage = ""
        guard !username.trimmingCharacters(in: .whitespaces).isEmpty,
              !password.trimmingCharacters(in: .whitespaces).isEmpty else {
            
            errorMessage = "Please fill in all fields."
            return false
        }
      //email@foo.com
      //guard username.contains("@") && username.contains(".") else {
      //errorMessage = "Please enter valid email."
      //return
      //}

        return true
    }
}
    
