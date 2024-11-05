# HadesC2

HadesC2 is a command-and-control (C2) interface designed for managing and interacting with a warshipping device. Built with Python, HadesC2 provides a secure and streamlined command center with user authentication, role-based access, and device management capabilities.

![HadesC2 ASCII Skull](https://your-image-url.com) *(optional: include an image of your ASCII art here)*

## Features

- **Admin Interface**: Create, edit, and manage users, including viewing logs.
- **Secure Authentication**: Passwords are encrypted using bcrypt, and hidden input prevents visible passwords.
- **Role-Based Access**: Admins have access to create users, view logs, and edit user accounts. Regular users have restricted device management options.
- **Device Management**: Control and monitor connected warshipping devices (with plans to integrate SSH communication).

## Requirements

- **Python 3.6+**
- **Dependencies**: Listed in `requirements.txt`

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/HadesC2.git
   cd HadesC2
