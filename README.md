# File Compressor Web Application

A Flask-based web application that allows users to upload multiple files, compress them into ZIP archives, and manage their compressed files with secure user authentication.

## Features

- **User Authentication**: Secure signup and login system
- **File Upload**: Upload multiple files at once
- **Automatic Compression**: Files are automatically compressed into ZIP archives
- **File Management**: View, download, and delete your compressed files
- **MongoDB Storage**: All files and user data stored in MongoDB
- **User Sessions**: Secure session management for authenticated users

## Prerequisites

Before running this application, make sure you have the following installed:

- Python 3.7+
- MongoDB 4.0+
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd file-compressor-app
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages**
   ```bash
   pip install flask pymongo werkzeug
   ```

4. **Start MongoDB**
   
   Make sure MongoDB is running on `localhost:27017`. If you need to start it:
   ```bash
   # On Linux/Mac
   sudo systemctl start mongod
   
   # On Windows
   net start MongoDB
   ```

## Configuration

The application uses the following default settings:

- **Port**: 4630
- **MongoDB URI**: `mongodb://localhost:27017`
- **Database Name**: `file_compressor_db`
- **Upload Folder**: `./uploads`
- **Secret Key**: `supersecretkey` (⚠️ Change this in production!)

### Important Security Note

Before deploying to production, you must:
1. Change the `app.secret_key` to a secure random string
2. Implement password hashing (currently passwords are stored in plain text)
3. Add proper input validation and sanitization
4. Configure MongoDB authentication

## Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Access the application**
   
   Open your web browser and navigate to:
   ```
   http://localhost:4630
   ```

3. **Create an account**
   - Click on "Sign Up"
   - Enter a username and password
   - Confirm your password

4. **Upload files**
   - Log in with your credentials
   - Select multiple files to upload
   - Files will be automatically compressed into a ZIP archive

5. **Manage files**
   - View all your uploaded ZIP files in "My Files"
   - Download any ZIP file
   - Delete files you no longer need

## Project Structure

```
file-compressor-app/
│
├── app.py                 # Main application file
├── uploads/              # Directory for uploaded files
├── templates/            # HTML templates
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   └── myfiles.html
└── README.md            # This file
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page (requires login) |
| `/signup` | GET, POST | User registration |
| `/login` | GET, POST | User login |
| `/logout` | GET | User logout |
| `/upload` | POST | Upload and compress files |
| `/myfiles` | GET | View user's files |
| `/download/<file_id>` | GET | Download a ZIP file |
| `/delete/<file_id>` | POST | Delete a file |

## Database Schema

### Users Collection
```javascript
{
  _id: ObjectId,
  username: String,
  password: String  // ⚠️ Plain text - should be hashed in production
}
```

### Files Collection
```javascript
{
  _id: ObjectId,
  username: String,
  filename: String,
  upload_time: DateTime,
  filedata: Binary
}
```

## Development

To run the application in debug mode:

```bash
python app.py
```

The application will automatically reload when you make changes to the code.

## Production Deployment

For production deployment, consider:

1. **Security Improvements**
   - Use `bcrypt` or `argon2` for password hashing
   - Change the secret key to a secure random value
   - Enable MongoDB authentication
   - Use environment variables for configuration

2. **Performance**
   - Use a production WSGI server (Gunicorn, uWSGI)
   - Consider using GridFS for large file storage
   - Implement file size limits
   - Add rate limiting

3. **Deployment Example with Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:4630 app:app
   ```

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running: `sudo systemctl status mongod`
- Check if the port 27017 is accessible
- Verify MongoDB URI in the code

### File Upload Issues
- Check folder permissions for the `uploads` directory
- Verify disk space availability
- Check file size limits (adjust if needed)

### Port Already in Use
- Change the port in `app.py`: `app.run(debug=True, port=YOUR_PORT)`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Flask framework
- MongoDB for database
- Python zipfile module for compression

## Contact

For questions or support, please open an issue in the GitHub repository.

---

**⚠️ Security Warning**: This application is for educational purposes. Before using in production, implement proper security measures including password hashing, input validation, CSRF protection, and secure session management.# file-compress-Datadrop-
