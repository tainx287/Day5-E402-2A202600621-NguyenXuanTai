import json
import os
import csv
import sys

# Reconfigure stdout/stderr to UTF-8 to prevent UnicodeEncodeError on Windows terminals
if sys.version_info >= (3, 7):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

DB_FILE = os.path.join(os.path.dirname(__file__), "mock_hotel_database.json")


def load_db():
    """Tải cơ sở dữ liệu từ tệp JSON."""
    if not os.path.exists(DB_FILE):
        raise FileNotFoundError(f"Không tìm thấy tệp cơ sở dữ liệu: {DB_FILE}")
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def search_rooms(guests=None, min_area=None, max_price=None, has_bathtub=False):
    """
    Tìm kiếm phòng nghỉ theo các tiêu chí lọc (Happy Path).
    """
    db = load_db()
    results = []
    
    for room in db.get("room_types", []):
        # 1. Kiểm tra sức chứa
        if guests is not None and room.get("max_guests", 0) < guests:
            continue
            
        # 2. Kiểm tra diện tích tối thiểu
        if min_area is not None and room.get("area_m2", 0) < min_area:
            continue
            
        # 3. Kiểm tra giá tối đa
        if max_price is not None and room.get("price_from", 0) > max_price:
            continue
            
        # 4. Kiểm tra tiện ích bồn tắm
        if has_bathtub:
            amenities_lower = [a.lower() for a in room.get("room_amenities", [])]
            # Kiểm tra xem có bồn tắm nằm trong danh sách tiện ích không
            has_tub = any("bồn tắm" in a or "bathtub" in a or "jacuzzi" in a for a in amenities_lower)
            if not has_tub:
                continue
                
        results.append(room)
        
    return results

def compare_rooms(room_id_1, room_id_2):
    """
    So sánh hai hạng phòng dựa trên các trường dữ liệu tĩnh.
    """
    db = load_db()
    rooms = {r["room_id"]: r for r in db.get("room_types", [])}
    
    r1 = rooms.get(room_id_1)
    r2 = rooms.get(room_id_2)
    
    if not r1 or not r2:
        return None
        
    comparison = {
        "fields": ["Tên phòng", "Giá tham khảo", "Diện tích (m2)", "Số khách tối đa", "Loại giường", "Tầm nhìn", "Bồn tắm nằm", "Ưu điểm nổi bật"],
        "room_1": {
            "name": r1["room_name"],
            "price": f"{r1['price_from']:,} VNĐ" if r1.get("price_from") else "Chưa cập nhật",
            "area": f"{r1['area_m2']} m2",
            "guests": f"{r1['max_guests']} người",
            "bed": r1["bed_type"],
            "view": r1["view"],
            "bathtub": "Có" if any("bồn tắm" in a.lower() or "bathtub" in a.lower() or "jacuzzi" in a.lower() for a in r1["room_amenities"]) else "Không",
            "notes": r1["notes"]
        },
        "room_2": {
            "name": r2["room_name"],
            "price": f"{r2['price_from']:,} VNĐ" if r2.get("price_from") else "Chưa cập nhật",
            "area": f"{r2['area_m2']} m2",
            "guests": f"{r2['max_guests']} người",
            "bed": r2["bed_type"],
            "view": r2["view"],
            "bathtub": "Có" if any("bồn tắm" in a.lower() or "bathtub" in a.lower() or "jacuzzi" in a.lower() for a in r2["room_amenities"]) else "Không",
            "notes": r2["notes"]
        }
    }
    return comparison

def get_amenity_info(amenity_query):
    """
    Tra cứu thông tin một tiện ích chung của khách sạn (Low-confidence Path).
    """
    db = load_db()
    query_lower = amenity_query.lower()
    
    # Tìm tiện ích phù hợp trong danh sách general_amenities
    for amenity in db.get("hotel_info", {}).get("general_amenities", []):
        if query_lower in amenity["amenity_name"].lower():
            return amenity
            
    return None

def get_nearby_places(category=None):
    """
    Lọc danh sách các địa điểm xung quanh khách sạn.
    """
    db = load_db()
    places = db.get("nearby_places", [])
    
    if category:
        places = [p for p in places if p["category"].lower() == category.lower()]
        
    return places

def search_policy_faq(query_text):
    """
    Tìm kiếm chính sách/FAQ dựa trên từ khóa đơn giản.
    """
    db = load_db()
    query_lower = query_text.lower()
    results = []
    
    for faq in db.get("policy_or_faq", []):
        if query_lower in faq["question"].lower() or query_lower in faq["answer"].lower():
            results.append(faq)
            
    return results

def export_to_csv():
    """
    Xuất dữ liệu từ JSON sang các tệp CSV để dễ dàng tải lên Google Sheets.
    """
    db = load_db()
    data_dir = os.path.dirname(DB_FILE)
    
    # 1. hotel_info.csv (Chứa thông tin chung khách sạn)
    hotel_info = db.get("hotel_info", {})
    hotel_info_file = os.path.join(data_dir, "hotel_info.csv")
    with open(hotel_info_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Field", "Value"])
        writer.writerow(["hotel_name", hotel_info.get("hotel_name")])
        writer.writerow(["short_description", hotel_info.get("short_description")])
        writer.writerow(["full_description", hotel_info.get("full_description")])
        writer.writerow(["address", hotel_info.get("address")])
        writer.writerow(["area", hotel_info.get("area")])
        writer.writerow(["checkin_time", hotel_info.get("checkin_time")])
        writer.writerow(["checkout_time", hotel_info.get("checkout_time")])
        writer.writerow(["general_images", ";".join(hotel_info.get("general_images", []))])
        writer.writerow(["hotel_policies_known", hotel_info.get("hotel_policies_known")])
    print(f"Đã xuất: {hotel_info_file}")

    # 2. hotel_amenities.csv (Tiện ích chung khách sạn)
    hotel_amenities_file = os.path.join(data_dir, "hotel_amenities.csv")
    with open(hotel_amenities_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["amenity_name", "available", "is_free", "fee_note", "applies_to_room", "source"])
        for amenity in hotel_info.get("general_amenities", []):
            writer.writerow([
                amenity.get("amenity_name"),
                amenity.get("available"),
                amenity.get("is_free"),
                amenity.get("fee_note"),
                amenity.get("applies_to_room"),
                amenity.get("source")
            ])
    print(f"Đã xuất: {hotel_amenities_file}")

    # 3. room_types.csv (Danh sách phòng ngủ)
    room_types_file = os.path.join(data_dir, "room_types.csv")
    with open(room_types_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["room_id", "room_name", "room_description", "price_from", "max_guests", "area_m2", "bed_type", "view", "room_amenities", "room_images", "notes"])
        for r in db.get("room_types", []):
            writer.writerow([
                r.get("room_id"),
                r.get("room_name"),
                r.get("room_description"),
                r.get("price_from"),
                r.get("max_guests"),
                r.get("area_m2"),
                r.get("bed_type"),
                r.get("view"),
                " | ".join(r.get("room_amenities", [])),
                ";".join(r.get("room_images", [])),
                r.get("notes")
            ])
    print(f"Đã xuất: {room_types_file}")

    # 4. nearby_places.csv (Địa điểm xung quanh)
    nearby_places_file = os.path.join(data_dir, "nearby_places.csv")
    with open(nearby_places_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["place_id", "place_name", "category", "distance", "short_description", "suitable_for", "source_note"])
        for p in db.get("nearby_places", []):
            writer.writerow([
                p.get("place_id"),
                p.get("place_name"),
                p.get("category"),
                p.get("distance"),
                p.get("short_description"),
                p.get("suitable_for"),
                p.get("source_note")
            ])
    print(f"Đã xuất: {nearby_places_file}")

    # 5. policy_or_faq.csv (Chính sách & FAQ)
    policy_or_faq_file = os.path.join(data_dir, "policy_or_faq.csv")
    with open(policy_or_faq_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["question", "answer", "category", "source", "confidence"])
        for faq in db.get("policy_or_faq", []):
            writer.writerow([
                faq.get("question"),
                faq.get("answer"),
                faq.get("category"),
                faq.get("source"),
                faq.get("confidence")
            ])
    print(f"Đã xuất: {policy_or_faq_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "export":
        export_to_csv()
    else:
        # CLI Demo mini để test các paths
        print("=== CHƯƠNG TRÌNH KIỂM THỬ DỮ LIỆU GIẢ LẬP ===")
        print("Đang tải dữ liệu khách sạn mẫu...")
        try:
            db = load_db()
            print(f"Tải thành công: {db['hotel_info']['hotel_name']}")
            print("-" * 50)
            
            # Demo 1: Happy Path - Lọc phòng
            print("[Path 1: Happy Path] Lọc phòng cho 2 người, có bồn tắm, diện tích >= 30m2:")
            matched_rooms = search_rooms(guests=2, min_area=30, has_bathtub=True)
            for room in matched_rooms:
                print(f" - {room['room_name']} ({room['area_m2']}m2) - Giá từ: {room['price_from']:,} VNĐ")
                print(f"   Ảnh phòng: {room['room_images'][0]}")
                print(f"   View: {room['view']}")
                
            print("-" * 50)
            # Demo 2: Low-confidence Path - Check phí tiện ích
            print("[Path 2: Low-confidence Path] Tra cứu tiện ích hồ bơi và đưa đón sân bay:")
            for item in ["Bể bơi vô cực", "Dịch vụ đưa đón sân bay", "Ăn sáng miễn phí"]:
                res = get_amenity_info(item)
                if res:
                    print(f" - Tiện ích: {res['amenity_name']}")
                    print(f"   Khả dụng: {'Có' if res['available'] else 'Không'}")
                    print(f"   Miễn phí: {'Có' if res['is_free'] else 'Không'}")
                    print(f"   Ghi chú phí: {res['fee_note']}")
                else:
                    print(f" - Tiện ích '{item}': Không có thông tin phí trong hệ thống (Cần liên hệ lễ tân).")
                    
            print("-" * 50)
            # Demo 3: FAQ & Policy Path - Tra cứu thú cưng / hút thuốc
            print("[Path 3: FAQ / Policy Path] Tra cứu chính sách vật nuôi & hút thuốc:")
            for policy in ["thú cưng", "hút thuốc"]:
                faqs = search_policy_faq(policy)
                for faq in faqs:
                    print(f" H: {faq['question']}")
                    print(f" Đ: {faq['answer']}")
                    print(f" Nguồn: {faq['source']} (Độ tin cậy: {faq['confidence']})")
            
        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")
