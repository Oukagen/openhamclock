# OpenHamClock

**A modern, open-source amateur radio dashboard - spiritual successor to HamClock**

*In memory of Elwood Downey, WB0OEW, creator of the original HamClock*

---

## Overview

OpenHamClock is a web-based kiosk-style application that provides real-time space weather, radio propagation information, and other data useful to amateur radio operators. It's designed to run on any platform with a web browser, with special consideration for Raspberry Pi deployments.

## Features

### Current Features (v1.0.0)

- **World Map with Day/Night Terminator**
  - Real-time gray line display
  - Sun position tracking
  - DE and DX location markers with path visualization

- **Time Displays**
  - UTC time (large, prominent display)
  - Local time with date
  - Uptime counter

- **Location Information**
  - DE (your location) with Maidenhead grid square
  - DX (target location) with grid square
  - Short path and long path bearing
  - Distance calculation
  - Sunrise/sunset times for both locations

- **Space Weather Panel**
  - Solar Flux Index (SFI)
  - Sunspot Number
  - K-Index and A-Index
  - X-Ray flux
  - Overall conditions assessment

- **Band Conditions**
  - Visual display for all HF bands
  - Color-coded conditions (Good/Fair/Poor)
  - VHF band status

- **DX Cluster Feed**
  - Live spot display (placeholder for API integration)
  - Frequency, callsign, comment, and time

- **POTA Activity**
  - Parks on the Air activator tracking
  - Reference, frequency, and mode display

### Planned Features (Roadmap)

- [ ] Live API integration for space weather (NOAA, hamqsl.com)
- [ ] Real DX cluster connectivity (Telnet/WebSocket)
- [ ] Live POTA/SOTA API integration
- [ ] Satellite tracking
- [ ] VOACAP propagation predictions
- [ ] Contest calendar integration
- [ ] Hamlib/flrig radio control
- [ ] Rotator control
- [ ] Customizable panel layout
- [ ] Multiple map projections
- [ ] ADIF log file integration
- [ ] RESTful API for external control
- [ ] Touch screen support
- [ ] Alarm/alert system

## Installation

### Option 1: Direct Browser Use

Simply open `index.html` in any modern web browser. No server required!

```bash
# Clone or download the files
firefox index.html
# or
chromium-browser index.html
```

### Option 2: Raspberry Pi Kiosk Mode

1. **Install Raspberry Pi OS** (Desktop version recommended)

2. **Copy OpenHamClock files**
   ```bash
   mkdir ~/openhamclock
   cp index.html ~/openhamclock/
   ```

3. **Run the setup script**
   ```bash
   chmod +x setup-pi.sh
   ./setup-pi.sh
   ```

4. **Manual Kiosk Setup** (alternative)
   ```bash
   # Install unclutter to hide mouse cursor
   sudo apt-get install unclutter

   # Create autostart entry
   mkdir -p ~/.config/autostart
   cat > ~/.config/autostart/openhamclock.desktop << EOF
   [Desktop Entry]
   Type=Application
   Name=OpenHamClock
   Exec=chromium-browser --kiosk --noerrdialogs --disable-infobars --incognito file:///home/pi/openhamclock/index.html
   EOF
   ```

### Option 3: Local Web Server

For advanced features (future API integrations), run with a local server:

```bash
# Python 3
cd openhamclock
python3 -m http.server 8080

# Then open http://localhost:8080
```

### Option 4: Electron Desktop App (Future)

Coming soon: Packaged desktop applications for Windows, macOS, and Linux.

## Configuration

Edit the following values in `index.html` to customize:

```javascript
// Your callsign
const [callsign, setCallsign] = useState('YOUR_CALL');

// Your location (lat, lon)
const [deLocation, setDeLocation] = useState({ lat: 39.7392, lon: -104.9903 });

// Default DX location
const [dxLocation, setDxLocation] = useState({ lat: 35.6762, lon: 139.6503 });
```

### Future Configuration File

A separate `config.js` will be provided for easier configuration:

```javascript
// config.js (coming soon)
export default {
  callsign: 'K0CJH',
  location: {
    lat: 39.7392,
    lon: -104.9903
  },
  theme: 'dark',
  panels: ['clock', 'map', 'weather', 'dx', 'bands'],
  // ... more options
};
```

## Display Resolutions

OpenHamClock is responsive and works at various resolutions:

| Resolution | Recommended Use |
|------------|-----------------|
| 800x480    | Small Pi displays, Inovato Quadra |
| 1024x600   | 7" Pi touchscreens |
| 1280x720   | HD ready monitors |
| 1600x960   | Recommended for full features |
| 1920x1080  | Full HD monitors |
| 2560x1440  | Large displays, high detail |

## API Data Sources (Planned)

| Data | Source | Status |
|------|--------|--------|
| Space Weather | NOAA SWPC | Planned |
| Band Conditions | hamqsl.com | Planned |
| DX Cluster | Various Telnet nodes | Planned |
| POTA | pota.app API | Planned |
| SOTA | sotawatch.org | Planned |
| Satellites | N2YO, CelesTrak | Planned |

## Technical Details

### Architecture

- **Frontend**: React 18 (single-file, no build required)
- **Styling**: CSS-in-JS with CSS variables for theming
- **Maps**: SVG-based rendering (no external tiles)
- **Data**: Currently static, API integration planned

### Browser Support

- Chrome/Chromium 80+
- Firefox 75+
- Safari 13+
- Edge 80+

### Dependencies

None! OpenHamClock loads React and Babel from CDN for simplicity.

For offline/airgapped deployments, download these files:
- react.production.min.js
- react-dom.production.min.js
- babel.min.js

## Contributing

Contributions are welcome! Areas where help is needed:

1. **API Integrations** - Connect to live data sources
2. **Satellite Tracking** - SGP4 propagator implementation
3. **Map Improvements** - Better landmass rendering, additional projections
4. **Testing** - Various Pi models and display sizes
5. **Documentation** - User guides, translations
6. **Design** - UI/UX improvements, accessibility

## License

MIT License - Free for personal and commercial use.

## Acknowledgments

- **Elwood Downey, WB0OEW** - Creator of the original HamClock. His work inspired thousands of amateur radio operators worldwide. Rest in peace, OM.
- **Amateur Radio Community** - For continued innovation and the spirit of experimentation.

## Contact

- **GitHub**: [github.com/your-repo/openhamclock](https://github.com)
- **Email**: your-email@example.com

---

**73 de K0CJH**

*"The original HamClock will cease to function in June 2026. OpenHamClock aims to carry on Elwood's legacy with a modern, open-source implementation that the community can maintain and improve together."*
