//
//  RegisterShiftLeadViewModel.swift
//  StarbucksFrontend
//
//  Created by Archita Nemalikanti on 1/7/25.
//

import Foundation

class RegisterShiftLeadViewModel: ObservableObject {
    @Published var name: String = ""
    @Published var email: String = ""
    @Published var password: String = ""
    @Published var username: String = ""
    @Published var starbucksLocation: String = ""
    
    
    init () {}
    
    func register (){
        guard validate() else {
            return
        }
        
        //create a user:
    }
    
    private func validate() -> Bool {
        guard !name.trimmingCharacters(in: .whitespaces).isEmpty,
              !email.trimmingCharacters(in: .whitespaces).isEmpty,
              !password.trimmingCharacters(in: .whitespaces).isEmpty,
              !username.trimmingCharacters(in: .whitespaces).isEmpty,
              !starbucksLocation.trimmingCharacters(in: .whitespaces).isEmpty else {
            return false
        }
        
        guard email.contains("@") && email.contains(".") else {
            return false
        }
           
        guard password.count >= 6 else {
            return false //password
        }
        return true
        
    }
    
    
    
}
