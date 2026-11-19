## 4.3. Vai trò của ngữ cảnh và phản hồi sửa lỗi
### 4.3.1. Diễn biến kết quả ở giai đoạn phát triển
Trên tập phát triển 21 đối tượng, cấu hình cơ sở đạt 51/105 lượt, cấu hình Council Standard đạt 73/105 lượt và cấu hình ngữ cảnh kết hợp phản hồi đạt 96/105 lượt trước tinh chỉnh. Sau tinh chỉnh trên hai đối tượng đã quan sát, kết quả tổng hợp đạt 98/105 lượt. Bảng 4.3 trình bày đồng thời mốc trước và sau tinh chỉnh để thể hiện quá trình phát triển phương pháp.

@table development | Bảng 4.3. Kết quả phát triển quy trình sinh và sửa kiểm thử

Nguồn: số liệu giai đoạn phát triển đã tổng hợp theo từng cấu hình. Các cấu hình có khác biệt về ngữ cảnh và xử lý phản hồi; kết quả không tách riêng tác động nhân quả của từng thành phần.

Ở cấu hình trước tinh chỉnh, 67 lượt đạt ngay lần sinh đầu và 29 lượt được sửa thành công, gồm 24 lượt ở vòng thứ nhất và 5 lượt ở vòng thứ hai. Sau tinh chỉnh, các số tương ứng là 70 lượt đạt ngay và 28 lượt sửa thành công, gồm 22 lượt ở vòng thứ nhất và 6 lượt ở vòng thứ hai. Phản hồi thực thi giúp khai thác các lần sinh chưa thành công, nhưng thành công sau sửa chưa tự chứng minh mọi điều kiện khẳng định giữ nguyên ý nghĩa.

@figure repair | Hình 4.2. Phân bổ kết quả theo lần sinh và vòng sửa lỗi trên tập phát triển

Nguồn: các mốc đạt đầu tiên trong dữ liệu phát triển. Hai cột biểu diễn cùng quy mô 105 lượt của hai phiên bản tổng hợp; không cộng chúng thành 210 lượt đánh giá độc lập.

Khảo sát loại bỏ thành phần trên sáu đối tượng cho thấy cấu hình đầy đủ đạt 5/6; không dùng phản biện sửa lỗi đạt 4/6; không dùng hướng dẫn giao diện theo thư viện đạt 4/6. Cấu hình không tự động bổ sung lệnh nhập mô-đun đạt 6/6, cao hơn cấu hình đầy đủ trong mẫu nhỏ này. Kết quả cho thấy cần đánh giá cả tác dụng phụ của xử lý bổ sung, thay vì mặc định mọi thành phần đều có lợi. Bảng chi tiết được đưa vào Phụ lục 2.

### 4.3.2. Các khảo sát hỗ trợ lựa chọn ngữ cảnh
Các khảo sát ở Bảng 4.4 được tập hợp trong cùng một mạch phân tích. Khảo sát đầu kiểm tra ngữ cảnh phụ thuộc; các khảo sát sau chuyển trọng tâm sang thiết lập và giới hạn độ lớn của bộ kiểm thử. Chúng phục vụ phát triển cấu hình, không được cộng vào hai đối chứng chính.

@table mechanisms | Bảng 4.4. Khảo sát bổ trợ về ngữ cảnh và thiết lập

Nguồn: kết quả của từng khảo sát. Hai cột số lượt đạt là các đối chứng nội bộ trong cùng hàng; tiêu chí giữa các hàng không hoàn toàn giống nhau.

Trong khảo sát đầu, việc thêm ngữ cảnh phụ thuộc chưa cải thiện kết quả: nhánh mã nguồn đạt 8/27, nhánh bổ sung phụ thuộc đạt 5/27. Kết quả cho thấy có thêm mã nguồn không đồng nghĩa với có ngữ cảnh phù hợp hơn. Ngữ cảnh dài hoặc yêu cầu tạo bộ kiểm thử lớn có thể làm tăng khó khăn về cách sử dụng giao diện và xây dựng điều kiện khẳng định.

Khảo sát tiếp theo dùng ba hàm kiểm thử nhỏ và thông tin thiết lập theo quy tắc chung, đạt 7/18 so với 5/18 của đối chứng. Sau hai đợt đánh giá nhiều dự án, một khảo sát phát triển trên toàn bộ 34 đối tượng đã quan sát tiếp tục bổ sung khai báo phụ trợ cùng mô-đun. Nhánh mã nguồn đạt 11/34 và nhánh ngữ cảnh kết hợp thiết lập đạt 12/34; độ phủ tương ứng là 17,50% và 19,52%. Phần ngữ cảnh phụ trợ thực sự có ở 17/34 đối tượng.

Mức tăng một lượt ở khảo sát sau cùng còn nhỏ. Hơn nữa, ngữ cảnh phụ trợ và thông tin thiết lập được thêm cùng nhau nên chưa tách được đóng góp riêng của truy vết AST. RQ2 vì vậy được trả lời ở mức định hướng: phản hồi thực thi và ngữ cảnh phù hợp hỗ trợ xử lý một số lỗi, nhưng cần đối chứng tách thành phần và phạm vi rộng hơn trước khi khẳng định lợi ích tổng quát.

### 4.3.3. Đối chiếu với các đợt đánh giá trước khi mở rộng toàn phạm vi
Hai đợt đối chứng trước ghi nhận 28/81 so với 36/81 lượt đạt trên 9 dự án, và 32/102 so với 34/102 trên 12 dự án khi bổ sung thiết lập. Chênh lệch cân bằng dự án lần lượt là 9,88 và 1,85 điểm phần trăm; cả hai khoảng tin cậy còn chứa không. Đây là bối cảnh phát triển dẫn tới nhu cầu đánh giá toàn bộ danh mục, không được cộng vào số lượt của đợt chính mới.

Bảng chi tiết của hai đợt được giữ ở phụ lục để đối chiếu. Bốn dự án trong đợt 12 dự án từng xuất hiện ở tập phát triển lịch sử. Phân tích hậu kiểm trên tám dự án còn lại có 19/72 và 24/72 lượt đạt, với khoảng tin cậy chênh lệch còn chứa không; kết quả này cũng không thay thế mẫu đầy đủ.


Phân tích thứ cấp trên khảo sát ban đầu giữ nguyên các ca kiểm thử đã chạy thành công trong bản sinh đầu tiên. Cả hai nhánh phục hồi được bộ không rỗng ở 25/27 lượt dự kiến; số ca giữ lại là 141/208 ở nhánh mã nguồn và 127/216 ở nhánh phụ thuộc. Đây là khả năng tận dụng từng ca kiểm thử, không thay đổi kết quả chính 8/27 và 5/27 của tiêu chí chấp nhận toàn bộ bộ kiểm thử.

Khảo sát đột biến trên tập con này lên lịch 18 lượt đột biến cho mỗi nhánh. Nhánh mã nguồn phát hiện 9, không phát hiện 6 và chưa thể kết luận 3; nhánh phụ thuộc có các số tương ứng là 11, 3 và 4. Phạm vi nhỏ và điều kiện chọn bộ kiểm thử thành công không cho phép diễn giải thành hiệu quả phát hiện lỗi của toàn bộ đầu ra mô hình.

