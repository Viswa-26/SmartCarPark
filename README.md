# Smart Car Parking System

## Introduction

The **Smart Car Parking System** is an innovative solution aimed at addressing the common problem of parking in crowded urban areas. This system helps users quickly find the nearest available parking spot while also simplifying the management of parking spaces for parking lot owners. The system integrates **Google Maps API**, **OpenCV**, and **Flask** to offer a seamless, efficient, and user-friendly experience.

## Features

- **For Users**:
  - Users can get directions to the nearest parking lot with available spaces using the **Google Maps API**.
  - Real-time availability of parking spaces is displayed to help users save time and reduce fuel wastage.
  
- **For Admins**:
  - Parking lot owners can efficiently manage parking spaces via an **admin panel**.
  - The system uses **Euclidean Distance** to allocate the nearest available parking space to incoming vehicles.
  
- **AI-Powered Parking Detection**:
  - The system uses **OpenCV** for real-time parking space detection to ensure maximum utilization of available spaces.

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask
- **AI**: OpenCV for parking space detection
- **Database**: SQLite
- **Hosting**: Render

## Login Details

There are two types of user logins available for the system:

1. **Staff (Admin)**:
   - **Username**: admin
   - **Password**: `123456@admin`
   - **Login Type**: staff

2. **User**:
   - **Username**: user
   - **Password**: `123456@user`
   - **Login Type**: user

Note: These login credentials are for demonstration purposes. Ensure to update the system with secure authentication before deploying it for real-world use.

🌐 Try it Live: https://smartcarpark.onrender.com 

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/Viswa-26/SmartCarPark.git
