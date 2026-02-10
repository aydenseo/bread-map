import json
import folium

def create_map():
    # Load data
    try:
        with open("bakeries.json", "r", encoding="utf-8") as f:
            bakeries = json.load(f)
    except FileNotFoundError:
        print("bakeries.json not found!")
        return

    if not bakeries:
        print("No bakeries found in data.")
        return

    print(f"Loaded {len(bakeries)} bakeries.")

    # Create map centered on Seoul
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

    # Add markers
    for bakery in bakeries:
        lat = bakery.get("lat")
        lon = bakery.get("lon")
        name = bakery.get("name")
        review_count = bakery.get("review_count")
        address = bakery.get("address")
        
        if lat and lon:
            popup_html = f"""
            <div style="width:200px">
                <h4>{name}</h4>
                <p><b>Reviews:</b> {review_count}</p>
                <p>{address}</p>
            </div>
            """
            
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{name} ({review_count} reviews)",
                icon=folium.Icon(color="orange", icon="cutlery", prefix='fa')
            ).add_to(m)

    # Save map
    output_file = "seoul_bakery_map.html"
    m.save(output_file)
    print(f"Map saved to {output_file}")

if __name__ == "__main__":
    create_map()
