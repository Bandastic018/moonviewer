# 🌕 MoonViewer

MoonViewer is a Django-based web application that provides detailed insights into the Moon's characteristics for a specific location and time. It calculates the Moon's phase, visibility, moonrise and moonset times, altitude, and viewing recommendations.

---

## 🚀 Features
- Calculate the Moon's **phase percentage** and **phase name**.
- Get **moonrise** and **moonset** times based on location and forecast time.
- Determine the **visibility** of the Moon at the specified time.
- Calculate the **Moon's altitude** in degrees and provide detailed viewing recommendations.
- Support for selecting locations by **world capitals** or **custom coordinates**.
- Basic interface with options to forecast future Moon details.

---

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
    git clone https://github.com/Bandastic018/moonviewer.git
   cd moonviewer

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv  
  `source venv/bin/activate`  # On Windows use `venv\Scripts\activate` # and on Windows with Git Bash use `source venv/Scripts/activate`

3. **Install the dependencies**:
   ```bash
         pip install -r requirements.txt
4. **Create a .env file in the project root directory and add the following**:
  DJANGO_SECRET_KEY=your-very-secret-key
  DJANGO_DEBUG=True
  DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

5. **Run the migrations**:
   ```bash
      python manage.py migrate

6. **Start the development server**:
   ```bash
      python manage.py runserver

7. **Visit the app in your browser**:
   ```bash
     http://127.0.0.1:8000


📜 Usage
- Select a location from the world capitals dropdown or enter custom coordinates.
- Specify a date and time for the forecast (UTC time).
- View the detailed Moon data, including phase, rise/set times, altitude, and visibility.


🖼️ Media
MoonViewer includes visual representations of the Moon's phases. Images are located in the moon/static/images/ directory.

💡 Future Enhancements
- Add an interactive map to select custom locations.
- Display Moon-related facts and trivia.
- Improve the visualization of Moon phases.


📖 Technologies Used
- Backend: Django (Python)
- Frontend: HTML, CSS (with static files)
- Geolocation: Geopy
- Astronomical Calculations: PyEphem


🛡️ Security
- Ensure DEBUG is set to False in production.
- Set SECRET_KEY and ALLOWED_HOSTS via environment variables.


🤝 Contributing
Contributions are welcome! Feel free to fork the project, create a branch, and submit a pull request.
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name

3. Commit your changes:
   ```bash
      git commit -m "Add feature-name"
4. Push to the branch:
   ```bash
  git push origin feature-name
5. Submit a pull request.


📜 License
This project is licensed under the MIT License. Feel free to use it responsibly.

🙌 Acknowledgments
- Ephem: For astronomical calculations.
- Geopy: For geolocation services.
- Django: The web framework powering this app.
- [Nasa Images](https://science.nasa.gov/moon/moon-phases): Images of moon phases from NASA science website.
- [Favicon Generator](https://favicon.io/favicon-generator) : Used for favicon

Next Plans
-Resolve discrepancies in Moon accuracy.
- Add real-time notifications for moon phases.
- Enhance UI with interactive moon tracking visuals.
- Support multiple languages for global users.




Contact
For inquiries or feedback, reach out to:
- Email: ibrahimmuhammad@gmail.com
- GitHub: Bandastic018




Enjoy exploring the Moon! 🌕✨


