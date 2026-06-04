# Thin SPEC — Hotel Amenities Q&A Chatbot

Thin SPEC không phải PRD đầy đủ. Đây là bản cam kết đủ rõ để sáng Day 06 nhóm build ngay.

---

## 1. Track, product/app và user

**Track:** Travel & Hospitality  

**Product/app thật:**  
Hotel Amenities Q&A Chatbot — chatbot hỏi đáp thông tin khách sạn, hạng phòng, tiện ích, ảnh, vị trí và địa điểm xung quanh dựa trên dữ liệu có cấu trúc của một khách sạn.

**Tên prototype đề xuất:** HotelInfo Assistant / Hotel Amenities Q&A Assistant  

**Data source M1:** Google Sheet hoặc JSON tĩnh do nhóm chuẩn bị, gồm:

- `hotel_info`: tên khách sạn, mô tả, địa chỉ, khu vực, ảnh chung, giờ check-in/check-out nếu có.
- `room_types`: tên phòng, mô tả, giá tham khảo nếu có, diện tích, số khách tối đa, loại giường, view, tiện ích trong phòng, ảnh riêng từng phòng.
- `hotel_amenities`: Wi-Fi, bữa sáng, hồ bơi, gym, spa, nhà hàng, bãi xe, lễ tân, giặt là, đưa đón sân bay nếu có.
- `nearby_places`: quán ăn, điểm tham quan, cửa hàng tiện lợi, ATM, nhà thuốc, khoảng cách và ghi chú ngắn.
- `policy_or_faq`: trẻ em, giường phụ, thú cưng, hút thuốc, phụ thu, accessibility nếu có dữ liệu.
- `source_note`: nguồn của từng thông tin, ví dụ official website, internal sheet, OTA copy, manual input.

**User cụ thể:**  
Khách du lịch Việt Nam hoặc khách quốc tế đang cân nhắc chọn một khách sạn cho chuyến đi ngắn ngày, chưa đặt phòng, đang ở bước so sánh phòng/tiện ích trước khi ra quyết định.

**User scenario cụ thể:**  
Một khách đi Hà Nội/Đà Nẵng 2–3 ngày, đang xem khách sạn trên OTA hoặc website khách sạn. Họ muốn hỏi nhanh bằng ngôn ngữ tự nhiên:

```text
Phòng nào hợp cho 2 người, có bồn tắm, từ 35m2 trở lên?
Bữa sáng/hồ bơi/gym có miễn phí không?
Deluxe và Premium khác nhau gì?
Ảnh này là ảnh phòng Deluxe hay ảnh chung khách sạn?
Gần khách sạn có quán ăn/điểm đi chơi nào trong 10 phút đi bộ không?
```

**Nhóm có phải user thật không? Nếu không, khác ở đâu?**  
Nhóm có thể đóng vai user thật ở giai đoạn self-use vì các thành viên đều có thể là người từng/đang tìm khách sạn khi đi du lịch. Tuy nhiên nhóm chưa đại diện hoàn toàn cho user thật vì:

- Nhóm biết trước scope và giới hạn của prototype nên có thể khoan dung hơn người dùng thật.
- Nhóm có xu hướng test theo tiêu chí sản phẩm, còn khách thật sẽ hỏi tự nhiên, viết tắt, thiếu dấu, đôi khi hỏi lẫn booking/chính sách/availability.
- Nhóm chưa đại diện cho lễ tân/khách sạn — người chịu trách nhiệm cập nhật data và xử lý khi bot không trả lời được.

**Cách bù khoảng cách này trước M1 Day 06:**  
Phỏng vấn/test nhanh ít nhất 3 người ngoài nhóm từng đặt khách sạn trong 6 tháng gần đây. Cho họ hỏi thử 5–7 câu về phòng/tiện ích, ghi lại câu nào bot trả lời được, câu nào thiếu data, câu nào ngoài scope.

---

## 2. Evidence summary

| Evidence | Nguồn | User/pain nói lên điều gì? | SPEC phải đổi gì? |
|---|---|---|---|
| Khi self-use trên OTA/website khách sạn, thông tin phòng, tiện ích, ảnh, chính sách và phí thường nằm rải ở nhiều khu vực: room card, facilities, FAQ, policy, gallery, review. Người dùng phải tự mở nhiều tab/màn hình để ghép thông tin. | Self-use evidence của nhóm trên Booking.com / Agoda / Traveloka / website khách sạn. Screenshot sẽ do nhóm tự chụp trong file Evidence Pack. | Pain không chỉ là “không có thông tin”, mà là “có thông tin nhưng phân mảnh, khó hỏi theo nhu cầu cá nhân”. | Build slice phải tập trung vào Q&A/so sánh phòng theo câu hỏi tự nhiên, không chỉ render lại danh sách tiện ích. Cần output dạng answer + room card + source. |
| Traveloka hotel pages thường có nhiều mục như room type, facilities, nearby places, reviews, policy/FAQ trên cùng một trang khách sạn. Đây là nguồn tốt để nhóm test điểm gãy “dữ liệu có nhưng người dùng phải tự dò”. | Traveloka hotel page ví dụ: https://www.traveloka.com/en-en/hotel/vietnam/valley-hotel--travel-9000000969729 | User cần truy vấn theo intent cụ thể như “phòng nào có bồn tắm”, “gần đó có gì”, “phòng nào phù hợp gia đình”, thay vì đọc toàn bộ trang. | Data M1 phải tách rõ `room_types`, `hotel_amenities`, `nearby_places`, `policy_or_faq` để bot retrieve đúng nhóm dữ liệu. |
| Booking.com AI Trip Planner cho phép traveler hỏi câu hỏi travel tổng quát/cụ thể và refine trong hội thoại. Điều này chứng minh hành vi hỏi bằng ngôn ngữ tự nhiên là hợp lý trong travel planning. | Booking.com News: https://news.booking.com/bookingcom-enhances-travel-planning-with-new-ai-powered-features--for-easier-smarter-decisions/ | User muốn hỏi theo ngôn ngữ tự nhiên, không muốn chỉ dùng filter/form cứng. | Prototype nên dùng LLM để hiểu câu hỏi tiếng Việt tự nhiên, viết tắt, không dấu; nhưng giới hạn retrieval trong data khách sạn đã cung cấp. |
| Expedia in ChatGPT cho phép hỏi đáp/travel planning bằng hội thoại, nhưng booking và kiểm tra chi tiết vẫn phụ thuộc luồng Expedia/nguồn ngoài. | Expedia in ChatGPT: https://www.expedia.com/product/expedia-in-chatgpt/ | AI hữu ích để khám phá/hỏi đáp, nhưng thông tin quan trọng như booking, giá, availability cần xác nhận ở hệ thống giao dịch. | SPEC phải chặn các intent booking/cancel/availability/real-time price. Bot chỉ hướng người dùng sang link booking/lễ tân nếu hỏi ngoài scope. |
| Review/complaint khách sạn ở Hà Nội và nguồn nghiệp vụ lễ tân cho thấy khách hay phàn nàn về phòng, phòng tắm, facilities, breakfast, location, reservation/promotion hoặc chất lượng phòng thực tế không đúng kỳ vọng. | Evidence Pack: public review/complaint research + Hoteljob.vn/front-desk complaint patterns. | Nếu thông tin phòng/tiện ích không rõ trước khi đặt, khách dễ kỳ vọng sai và mất niềm tin khi nhận phòng. | SPEC phải ưu tiên trust: show source, phân biệt ảnh chung/ảnh phòng, nói rõ free/paid/unknown, không bịa chính sách hoặc tiện ích. |
| Bằng chứng từ self-use cho thấy câu hỏi có ngày cụ thể như “15/06 còn phòng không?” buộc người dùng vào availability/booking flow. Đây không phải dữ liệu tĩnh. | Self-use evidence trên OTA/booking flow. | User thường trộn câu hỏi thông tin với câu hỏi giao dịch. Nếu bot trả lời bừa về còn phòng/giá theo ngày sẽ gây rủi ro cao. | Thêm Failure path bắt buộc: detect date/availability/booking/cancel/change intent và fallback rõ ràng. |

---

## 3. Pain statement

```text
User khách du lịch đang gặp khó ở bước tìm hiểu và so sánh thông tin phòng/tiện ích trước khi chọn khách sạn,
vì thông tin về hạng phòng, diện tích, ảnh, tiện ích, phí, chính sách và địa điểm xung quanh bị rải ở nhiều tab/mục khác nhau trên OTA hoặc website khách sạn,
dẫn tới họ mất thời gian tự đọc, tự so sánh, dễ hiểu nhầm ảnh/tiện ích/phí và có thể chọn sai phòng so với nhu cầu.
Bằng chứng chính là self-use observation trên các app/web OTA, nơi nhóm phải mở room card/facilities/FAQ/gallery/policy để trả lời các câu hỏi như “phòng nào có bồn tắm từ 35m2”, “bữa sáng có miễn phí không”, “ảnh này thuộc phòng nào”, cùng với evidence public về complaint khách sạn liên quan đến room/facilities/breakfast/location.
```

**Pain gói gọn trong 1 câu:**  
Khách không thiếu dữ liệu khách sạn; họ thiếu một cách hỏi nhanh, đáng tin và có nguồn để biến dữ liệu rời rạc thành quyết định chọn phòng đúng.

---

## 4. Build slice

```text
Cho khách du lịch đang tìm hiểu khách sạn và so sánh hạng phòng/tiện ích trước khi đặt,
prototype sẽ dùng AI để tự động hiểu câu hỏi tự nhiên và truy xuất thông tin từ Google Sheet/JSON của khách sạn,
tạo ra câu trả lời ngắn gọn có source, room/amenity card, ảnh liên quan và lý do gợi ý,
và xử lý failure mode như hỏi ngày còn phòng, đặt/hủy/đổi phòng, giá real-time hoặc thiếu dữ liệu bằng cách từ chối trong phạm vi an toàn, nói rõ bot chưa có dữ liệu, hiển thị source hiện có và hướng người dùng sang booking link/lễ tân.
```

### Build slice cụ thể cho Day 06

**Prototype phải làm được:**

1. Người dùng hỏi thông tin khách sạn bằng tiếng Việt tự nhiên.
2. Bot phân loại intent vào một trong các nhóm:
   - `hotel_general_info`
   - `room_search`
   - `room_compare`
   - `room_detail`
   - `hotel_amenity`
   - `nearby_place`
   - `policy_or_faq`
   - `out_of_scope_booking`
   - `out_of_scope_availability`
   - `unknown_or_missing_data`
3. Bot retrieve đúng dữ liệu từ Google Sheet/JSON.
4. Bot trả lời có cấu trúc:
   - Câu trả lời trực tiếp.
   - Dữ liệu chính: tên phòng/tiện ích/địa điểm, diện tích, số khách, giá tham khảo nếu có, tiện ích liên quan.
   - Ảnh nếu có.
   - Source hoặc field nguồn.
   - Confidence/ghi chú nếu thiếu dữ liệu.
5. Bot không trả lời các nghiệp vụ ngoài scope:
   - Đặt phòng.
   - Hủy phòng.
   - Đổi ngày.
   - Check phòng trống theo ngày.
   - Xác nhận giá real-time.
   - Hoàn tiền/thanh toán.

**Prototype chưa cần làm:**

- Đăng nhập user.
- Kết nối OTA/PMS/channel manager.
- Booking engine.
- Payment.
- Tự động nhắn lễ tân.
- Web scraping realtime.
- Tự cập nhật giá/phòng trống.

### Output tối thiểu cần demo

```text
User hỏi:
“Phòng nào phù hợp cho 2 người, có bồn tắm, từ 35m2 trở lên?”

Bot trả lời:
- Gợi ý 1–2 phòng phù hợp.
- Nêu lý do match: max_guests, area_m2, bathtub, bed_type, price_from nếu có.
- Hiển thị ảnh phòng nếu có.
- Ghi source: room_types sheet / official hotel data.
- Nếu thiếu dữ liệu bồn tắm hoặc ảnh, nói rõ “chưa có dữ liệu”, không đoán.
```

---

## 5. Auto/Aug decision

Chọn một:

- [ ] **Augmentation:** AI gợi ý/draft/phân loại, user quyết cuối.
- [x] **Conditional automation:** AI tự làm trong case hẹp; case mơ hồ/rủi ro chuyển người.
- [ ] **Automation:** AI tự quyết và tự hành động.

**Lý do chọn:**  
Chọn **Conditional automation** vì bot có thể tự trả lời các câu hỏi thông tin hẹp nếu dữ liệu đã có trong Google Sheet/JSON, ví dụ tiện ích, diện tích, sức chứa, ảnh, mô tả phòng, địa điểm xung quanh. Nhưng với câu hỏi mơ hồ, thiếu dữ liệu, có rủi ro giao dịch hoặc cần dữ liệu realtime như availability/booking/cancel/đổi ngày/giá theo ngày, bot phải dừng lại và fallback.

Đây không phải Automation đầy đủ vì bot không tự quyết định booking, không giữ phòng, không thanh toán, không hủy/đổi đặt phòng và không thay nhân viên xử lý nghiệp vụ.

**Human role:**  
Reviewer / decider / trainer / rescuer

- **User là decider:** khách tự quyết có chọn phòng/khách sạn hay không.
- **Nhóm/hotel staff là trainer:** cập nhật Google Sheet/JSON, bổ sung field thiếu, sửa câu trả lời sai.
- **Hotel staff là rescuer:** xử lý booking, availability, hủy/đổi, câu hỏi nhạy cảm hoặc thiếu dữ liệu.
- **Nhóm là reviewer trong M1:** kiểm thử bot có trả lời đúng source, đúng boundary và không hallucinate không.

---

## 6. Four paths

| Path | Prototype phải thể hiện gì? |
|---|---|
| Happy | User hỏi câu nằm trong data, ví dụ “Phòng nào hợp cho 2 người, có bồn tắm, từ 35m2 trở lên?” Bot hiểu intent `room_search`, lọc đúng phòng, trả về 1–3 gợi ý kèm lý do match, ảnh phòng, diện tích, sức chứa, tiện ích liên quan, giá tham khảo nếu có và source. |
| Low-confidence | User hỏi câu có một phần thiếu hoặc không chắc, ví dụ “Bữa sáng, hồ bơi, gym có miễn phí không?” Data có `available=true` nhưng thiếu `is_free` hoặc `fee_note`. Bot trả lời phần biết chắc, đánh dấu phần chưa có dữ liệu, không đoán phí, đề xuất kiểm tra với lễ tân/official source. |
| Failure | User hỏi ngoài scope hoặc cần realtime/giao dịch, ví dụ “Ngày 15/06 còn phòng Deluxe không?”, “Đặt giúp tôi phòng này”, “Hủy booking giúp tôi”. Bot nhận diện `out_of_scope_availability` hoặc `out_of_scope_booking`, không trả lời bừa, không nhận thao tác, giải thích ngắn rằng prototype chỉ hỗ trợ hỏi đáp thông tin khách sạn/phòng/tiện ích và hướng sang booking link/lễ tân. |
| Correction | User phát hiện thông tin sai/thiếu, ví dụ “Không đúng, phòng Premium có bồn tắm mà”, hoặc admin thêm data mới. Bot không tự khẳng định lại nếu source chưa cập nhật; bot ghi nhận correction, hiển thị “cần kiểm tra/cập nhật data”, log vào `unanswered_or_correction_log` gồm câu hỏi, field thiếu/sai, source cần sửa, owner phụ trách. |

### Demo script ngắn cho từng path

**Happy path demo:**

```text
User: Phòng nào phù hợp cho 2 người, có bồn tắm, diện tích từ 35m2 trở lên?
Expected bot: Gợi ý phòng Premium/Executive nếu data match. Có lý do match và ảnh phòng.
```

**Low-confidence path demo:**

```text
User: Hồ bơi với gym có miễn phí không?
Expected bot: Nếu data chỉ có “có hồ bơi/gym” nhưng thiếu phí, bot nói chưa có dữ liệu phí. Không nói miễn phí nếu sheet không có `is_free=true`.
```

**Failure path demo:**

```text
User: Ngày 15/06 còn phòng Deluxe không? Đặt luôn giúp tôi.
Expected bot: Từ chối check/đặt vì cần availability realtime và booking system. Hướng sang booking link/lễ tân.
```

**Correction path demo:**

```text
User: Ảnh này không phải phòng Deluxe, đây là ảnh phòng Suite.
Expected bot: Ghi nhận correction, không dùng ảnh đó để đại diện Deluxe nữa trong phiên demo nếu có cơ chế state; log lỗi `room_image_mismatch` để owner sửa data.
```

---

## 7. Failure mode nguy hiểm nhất

```text
Nếu user hỏi câu có ngày cụ thể hoặc ý định giao dịch, ví dụ “Ngày 15/06 còn phòng Deluxe không?”, “Giá phòng này tối nay bao nhiêu?”, “Đặt luôn phòng này cho tôi”,
AI có thể hallucinate rằng còn phòng, đưa giá sai hoặc khiến user tưởng bot đã giữ/đặt phòng,
hậu quả là user ra quyết định sai, mất niềm tin, khách sạn bị khiếu nại hoặc phải xử lý kỳ vọng sai khi khách liên hệ/đến nhận phòng.
Prototype sẽ xử lý bằng detect intent availability/booking/real-time price, từ chối trong phạm vi an toàn, nói rõ “mình chưa có dữ liệu phòng trống/giá realtime và không thể đặt phòng”, hiển thị thông tin tĩnh đang có, kèm hướng dẫn chuyển sang booking link/lễ tân/OTA để xác nhận.
Owner kiểm thử path này là [TODO: tên thành viên phụ trách QA/failure path].
```

### Acceptance criteria cho failure mode này

Bot chỉ được pass nếu:

- Không nói “còn phòng” hoặc “hết phòng” khi không có availability API.
- Không báo giá theo ngày nếu data chỉ là giá tham khảo.
- Không dùng từ gây hiểu nhầm như “đã đặt”, “đã giữ phòng”, “booking thành công”.
- Có câu fallback rõ ràng trong tối đa 2–3 câu.
- Có gợi ý kênh xử lý đúng: booking link/lễ tân/OTA.
- Có log câu hỏi ngoài scope để nhóm biết user hay hỏi gì.

### Câu fallback chuẩn

```text
Mình chưa có dữ liệu phòng trống/giá realtime và không thể đặt, hủy hoặc đổi phòng trong prototype này. Mình chỉ có thể hỗ trợ thông tin tĩnh về khách sạn, hạng phòng, tiện ích, ảnh và địa điểm xung quanh. Để xác nhận còn phòng hoặc đặt phòng, bạn vui lòng kiểm tra trên link booking chính thức hoặc liên hệ lễ tân.
```

---

## 8. Cam kết scope để Day 06 build ngay

### In scope

- Q&A thông tin khách sạn.
- Q&A tiện ích chung.
- Q&A hạng phòng.
- So sánh 2 hạng phòng.
- Gợi ý phòng theo tiêu chí đơn giản.
- Hiển thị ảnh chung/ảnh phòng nếu data có.
- Hỏi đáp tiện ích xung quanh nếu data curated có.
- Fallback ngoài scope.
- Log câu hỏi thiếu data/correction.

### Out of scope

- Booking.
- Availability theo ngày.
- Giá realtime.
- Hủy/đổi/hoàn tiền.
- Thanh toán.
- Xử lý booking số lượng lớn.
- Tư vấn itinerary phức tạp.
- Tự scrape web realtime.
- Tự gọi điện/nhắn lễ tân.

### Metric đánh giá M1

```text
Success metric chính:
- Bot trả lời đúng >= 80% bộ test 20 câu nằm trong scope.
- 100% câu hỏi booking/availability/cancel/change phải bị fallback đúng.
- 0 câu trả lời bịa tiện ích/phí/giá/phòng trống khi data không có.
- Với mỗi câu trả lời về phòng/tiện ích, bot phải show ít nhất 1 source hoặc field nguồn.

Secondary metric:
- User test ngoài nhóm chọn được phòng phù hợp nhanh hơn so với tự đọc OTA/website.
- Ít nhất 3 câu hỏi thiếu data được log để cải thiện Google Sheet/JSON.
```

### Owner/test plan đề xuất

| Hạng mục | Owner | Cách test |
|---|---|---|
| Happy path room search | [TODO] | Test 5 câu lọc phòng theo số người, diện tích, tiện ích, giá tham khảo. |
| Room comparison | [TODO] | Test 3 câu so sánh Deluxe/Premium/Suite. |
| Amenity free/paid/unknown | [TODO] | Test 5 câu về breakfast, pool, gym, spa, parking, airport pickup. |
| Nearby places | [TODO] | Test 3 câu về ăn uống/đi chơi/ATM/nhà thuốc gần khách sạn. |
| Failure path booking/availability | [TODO] | Test 5 câu có ngày cụ thể, đặt/hủy/đổi phòng, giá tối nay. |
| Correction log | [TODO] | Test 2 câu user báo sai ảnh/sai tiện ích để xem bot có log không. |
