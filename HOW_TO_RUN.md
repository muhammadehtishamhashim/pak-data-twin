# Pakistan Data Twin Dashboard - Quick Start

## 🚀 How to Run

Simply run:
```bash
streamlit run app.py
```

That's it! The app now includes:
1. **Landing Page** - Beautiful welcome screen with overview
2. **Dashboard** - Full analytics across all sectors

## 📱 How It Works

### Landing Page (First View)
- Clean welcome container with Pakistan flag
- "GET STARTED" button prominently displayed
- Overview of all dashboards
- Pakistan statistics visualization
- Technology stack showcase

### Dashboard (After GET STARTED)
- Sidebar appears with navigation
- Access to all 4 sectors:
  - 📈 Economy
  - 🎓 Education
  - ⚡ Energy
  - 🏥 Health
- "BACK TO HOME" button to return to landing page

## ✨ Features

- **Single App**: Everything in one `app.py` file
- **No Sidebar on Landing**: Clean first impression
- **Session State Navigation**: Smooth transitions
- **Integrated Design**: Consistent styling throughout
- **No Extra Windows**: Everything in the same tab

## 🎨 Design Highlights

- White container with minimal green borders (4px)
- Pakistan flag green (#0f4c3a) as primary color
- Clean, professional layout
- Responsive design
- Interactive visualizations

## 📁 Project Structure

```
pak-data-twin/
├── app.py                    # Main application (landing + dashboard)
├── dashboard_pages/
│   ├── economy.py           # Economy analytics
│   ├── education.py         # Education analytics
│   ├── energy.py            # Energy analytics
│   └── health.py            # Health analytics
├── datasets_cleaned/        # Processed datasets
├── saved_plots/             # Pre-generated forecast plots
└── .streamlit/
    └── config.toml          # Streamlit configuration
```

## 🔧 Configuration

The app uses session state to manage navigation:
- `show_landing`: Controls landing page visibility
- `current_page`: Tracks which dashboard is active

## 💡 Tips

- The landing page is hidden once you click "GET STARTED"
- Use "BACK TO HOME" in the sidebar to return to landing page
- All navigation happens within the same window
- No need for multiple Streamlit instances

## 🎯 Next Steps

After running the app:
1. View the landing page
2. Click "GET STARTED"
3. Explore the dashboards using sidebar navigation
4. Return home anytime with "BACK TO HOME"

Enjoy exploring Pakistan's data! 🇵🇰
