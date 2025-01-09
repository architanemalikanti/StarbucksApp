//
//  SBButton.swift
//  StarbucksFrontend
//
//  Created by Archita Nemalikanti on 1/6/25.
//

import SwiftUI

struct SBButton: View {
    let title: String
    let background: Color
    let action: () -> Void
    
    var body: some View {
        Button {
            // Action that occurs when button is tapped
            action()
        } label: {
            ZStack {
                RoundedRectangle(cornerRadius: 10)
                    .foregroundColor(background)
                    .frame(height: 50)
                
                Text(title)
                    .foregroundColor(Color.white)
                    .bold()
            }
        }
        
    }
}

#Preview {
    SBButton(title: "Value", background: .pink, action: {
        print("Button tapped")
    })
}
