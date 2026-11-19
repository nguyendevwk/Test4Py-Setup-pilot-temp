# MỞ ĐẦU
## 1. Lý do chọn đề tài
Kiểm thử đơn vị giúp phát hiện thay đổi ngoài ý muốn khi phần mềm được sửa đổi. Với Python, một ca kiểm thử có ích phải đồng thời gọi đúng giao diện, tạo được trạng thái đầu vào hợp lệ và kiểm tra kết quả có ý nghĩa. Mô hình ngôn ngữ lớn có thể hỗ trợ viết mã kiểm thử, nhưng việc chỉ cung cấp phần thân hàm thường chưa đủ để đáp ứng ba yêu cầu này. Các thông tin quan trọng có thể nằm trong hàm phụ trợ, cấu trúc đối tượng hoặc quy ước sử dụng của thư viện.

Một ví dụ cụ thể là lớp GentyArgs của thư viện genty. Kiểm tra các thuộc tính lưu đối số chưa bao quát hành vi duyệt đối số. Muốn kiểm tra hành vi đó, bộ kiểm thử cần biết quy tắc định dạng giá trị và thứ tự của đối số từ khóa. Một bộ kiểm thử có thể chạy thành công nhưng vẫn bỏ sót sai lệch ở phần hành vi chưa được kiểm tra. Bài toán nghiên cứu vì vậy không chỉ là tạo mã chạy được, mà là cung cấp đủ ngữ cảnh để sinh được kiểm thử thực thi đúng và có khả năng nhận biết thay đổi hành vi.

Test4Py giải quyết khó khăn về đầu vào cho Python bằng đồ thị gọi hàm, suy luận kiểu dựa trên hành vi và quy trình sửa kiểm thử lặp [1]. Trên cơ sở bài toán đó, đề tài khảo sát một hướng tiếp cận gọn hơn: kết hợp ngữ cảnh mã nguồn có giới hạn, thông tin thiết lập đã được thực thi thử và phản hồi từ môi trường kiểm thử. Hướng tiếp cận được gọi là Council trong báo cáo. Tên gọi này chỉ quy trình sinh và phản biện kiểm thử, không hàm ý đã đạt kết quả tốt nhất hiện có.

## 2. Mục tiêu và câu hỏi nghiên cứu
Mục tiêu của đề tài là xây dựng và đánh giá quy trình hỗ trợ sinh, sửa kiểm thử đơn vị cho các hàm và lớp Python trong điều kiện tài nguyên suy luận hạn chế. Nghiên cứu tập trung vào bốn câu hỏi nghiên cứu (research question, viết tắt RQ) sau.

RQ1. Việc bổ sung thông tin thiết lập đã được thực thi thử có cải thiện tỷ lệ bộ kiểm thử đạt yêu cầu và độ phủ so với chỉ cung cấp mã nguồn trên nhiều dự án hay không?

RQ2. Ngữ cảnh mã nguồn và phản hồi thực thi đóng góp như thế nào vào quá trình sinh và sửa kiểm thử?

RQ3. Các kiểm thử thu được có chạy lại ổn định và phát hiện được thay đổi hành vi trong phạm vi đánh giá hay không?

RQ4. Quy trình có khả thi về tài nguyên, chi phí suy luận và khả năng tái sử dụng kết quả hay không?

## 3. Đối tượng và phạm vi nghiên cứu
Đối tượng nghiên cứu là bộ kiểm thử do mô hình ngôn ngữ sinh cho các hàm và lớp thuộc thư viện Python công khai. Nguồn đối tượng được xác định từ các bộ chuẩn đánh giá (benchmark) và danh mục mô-đun liên quan. Phạm vi thực nghiệm gồm giai đoạn phát triển trên 21 đối tượng; hai đợt đánh giá thành phần trên 27 đối tượng thuộc 9 dự án và 34 đối tượng thuộc 12 dự án; cùng các khảo sát bổ trợ về ngữ cảnh, sửa lỗi và ngân sách đầu ra. Các đợt có thiết kế khác nhau được dùng để trả lời các khía cạnh tương ứng của cùng bài toán, không cộng thành một mẫu thống kê đồng nhất.

Qwen2.5-Coder-14B-Instruct lượng tử hóa 4 bit theo định dạng NormalFloat (NF4) đã được thực thi trên Kaggle trong giai đoạn đầu. Sau khi gặp hạn chế bộ nhớ và thời gian khởi tạo, nghiên cứu tiếp tục với GPT-OSS-20B qua Groq để hoàn thành đánh giá nhiều dự án. Hai cấu hình suy luận được trình bày theo vai trò trong tiến trình nghiên cứu, không dùng làm đối chứng trực tiếp về chất lượng mô hình.

## 4. Phương pháp nghiên cứu
Nghiên cứu kết hợp phân tích tài liệu, thiết kế quy trình sinh kiểm thử, thực nghiệm đối chứng ghép cặp và nghiên cứu trường hợp. Trong đối chứng ghép cặp, hai cấu hình được áp dụng cho cùng đối tượng với cùng mô hình, ngân sách đầu ra và tiêu chí đánh giá. Kết quả được phân tích theo dự án để phản ánh sự phụ thuộc giữa nhiều đối tượng thuộc cùng một thư viện. Khả năng tái sử dụng được đánh giá bằng chạy lại các kiểm thử đã lưu và khảo sát một số biến đổi hành vi có kiểm soát.

## 5. Bố cục báo cáo
Chương 1 xác định bài toán và vị trí của hướng tiếp cận. Chương 2 trình bày cơ sở lý thuyết. Chương 3 mô tả phương pháp và thiết kế đánh giá. Chương 4 phân tích kết quả theo bốn câu hỏi nghiên cứu. Chương 5 tổng hợp đóng góp và định hướng mở rộng. Các mẫu lời nhắc, bảng chi tiết và hồ sơ tái lập được đưa vào phụ lục.

# CHƯƠNG 1. TỔNG QUAN NGHIÊN CỨU
## 1.1. Bài toán sinh kiểm thử cho thư viện Python
Một thư viện Python có thể xuất cùng một lớp qua nhiều đường dẫn, chấp nhận đối tượng theo giao diện hành vi và thay đổi chữ ký thông qua hàm trang trí. Vì vậy, thông tin về tên và tham số của một hàm chưa luôn đủ để tạo dữ liệu đầu vào hợp lệ. Những lỗi như nhập sai mô-đun, tạo đối tượng thiếu trạng thái hoặc kỳ vọng sai kiểu giá trị thường xuất hiện trước khi kiểm thử chạm tới hành vi cần đánh giá.

Trong báo cáo, mỗi đối tượng kiểm thử là một hàm hoặc lớp được lựa chọn theo tiêu chí của từng tập đánh giá. Một lượt sinh tạo ra một bộ kiểm thử cho đối tượng đó. Phân biệt hai đơn vị này giúp tránh nhầm nhiều lần gọi mô hình với nhiều đối tượng hoặc nhiều dự án độc lập.

## 1.2. Các hướng tiếp cận liên quan
Kiểm thử dựa trên tìm kiếm, điển hình là Pynguin, tìm kiếm dữ liệu và chuỗi lời gọi nhằm tăng độ phủ [2]. Hướng tiếp cận này tận dụng phản hồi cấu trúc nhưng việc tạo đối tượng phù hợp và xác định kết quả mong đợi vẫn là thách thức đối với Python.

Các phương pháp dựa trên mô hình ngôn ngữ khai thác tên gọi, tài liệu và mã nguồn để sinh kiểm thử có cấu trúc gần với cách viết của lập trình viên. ChatUniTest kết hợp sinh, kiểm tra và sửa lỗi trong một quy trình phản hồi [3]. CoverUp sử dụng thông tin độ phủ để định hướng bổ sung kiểm thử Python [4]. Các công trình này cho thấy lợi ích của việc kết nối mô hình với môi trường thực thi thay vì chỉ đánh giá câu trả lời dưới dạng văn bản.

Test4Py đặc biệt chú trọng tính phù hợp của đầu vào trong Python. Phương pháp sử dụng đồ thị gọi hàm để bổ sung ngữ cảnh tham số, suy luận kiểu dựa trên hành vi và sửa kiểm thử theo vòng lặp [1]. Đề tài kế thừa vấn đề nghiên cứu này nhưng thu hẹp trọng tâm vào thông tin giao diện, thiết lập đầu vào và ngữ cảnh phụ trợ có giới hạn.

@table related | Bảng 1.1. Vị trí của hướng tiếp cận trong các nghiên cứu sinh kiểm thử

Nguồn: tổng hợp từ [1], [2], [3], [4]. Bảng so sánh cơ chế, không phải bảng xếp hạng thực nghiệm giữa các công cụ.

## 1.3. Hướng cải tiến được khảo sát
Thông tin bổ sung chỉ có ích khi liên quan tới hành vi cần kiểm tra và đủ ngắn để mô hình sử dụng được. Đề tài khảo sát ba cơ chế: bổ sung khai báo phụ trợ từ mã nguồn, cung cấp thiết lập đầu vào đã được thực thi thử và sử dụng kết quả chạy kiểm thử để định hướng sửa lỗi. Mục đích là giảm sai sót về giao diện và trạng thái, đồng thời giữ ngân sách suy luận nhỏ.

Thông tin thiết lập cho biết một cách gọi đã hoàn tất trong môi trường đánh giá; thông tin này không cung cấp giá trị đầu ra mong đợi cho kiểm thử. Phân biệt giữa thông tin về cách sử dụng và điều kiện khẳng định giúp hạn chế việc đưa sẵn đáp án kiểm thử vào ngữ cảnh.

Đóng góp được đánh giá ở mức thành phần và quy trình ứng dụng. Đổi dịch vụ suy luận là lựa chọn triển khai để thu thập số liệu, còn nội dung phương pháp nằm ở cách lựa chọn ngữ cảnh, tổ chức phản hồi và đánh giá chất lượng kiểm thử.

## 1.4. Tiến trình nghiên cứu và lựa chọn mô hình
Giai đoạn đầu triển khai Qwen2.5-Coder-14B-Instruct với lượng tử hóa NF4 trên hai bộ xử lý đồ họa (GPU) T4 của Kaggle. Sau điều chỉnh cơ chế attention, bốn phép kiểm tra bộ nhớ với 4.096 token đầu vào và 512 token đầu ra đều hoàn tất. Tuy nhiên, khởi tạo từ đầu tiêu tốn phần lớn thời lượng của lượt chạy. Việc tái sử dụng kết quả của các bước khởi tạo trùng khớp giúp lượt chạy sau hoàn tất, đồng thời tạo ra các kiểm thử được giữ lại để đánh giá ứng dụng.

GPT-OSS-20B qua Groq được sử dụng ở giai đoạn tiếp theo để giảm gánh nặng vận hành mô hình cục bộ và mở rộng số dự án. Kết quả 14B tiếp tục đóng vai trò bằng chứng về triển khai và tái sử dụng kiểm thử; kết quả Groq cung cấp đối chứng thành phần trên phạm vi rộng hơn. Cách tổ chức này giữ được đóng góp của hai giai đoạn mà không quy chênh lệch kết quả cho riêng mô hình hoặc hạ tầng.

# CHƯƠNG 2. CƠ SỞ LÝ THUYẾT
## 2.1. Cấu trúc kiểm thử đơn vị và cơ sở xác định kết quả mong đợi
Một ca kiểm thử thường gồm ba bước: chuẩn bị dữ liệu và trạng thái, gọi chức năng cần kiểm tra, rồi đối chiếu kết quả thực tế với điều kiện khẳng định. Cơ sở xác định kết quả mong đợi được gọi là test oracle. Trong kiểm thử sinh tự động, một lời gọi không phát sinh ngoại lệ chưa đủ để xác nhận hành vi đúng; bộ kiểm thử còn phải kiểm tra thuộc tính có ý nghĩa đối với chức năng [14], [18].

Python là ngôn ngữ định kiểu động. Ngoài ra, nhiều thư viện chấp nhận đối tượng theo tập hành vi mà đối tượng hỗ trợ, thường được gọi là duck typing. Hai đặc điểm này có liên quan nhưng không đồng nhất. Kiểm thử cần đáp ứng giao diện được sử dụng tại thời điểm chạy, thay vì chỉ khớp một tên kiểu được suy đoán.

## 2.2. Ngữ cảnh mã nguồn và thông tin thiết lập
Cây cú pháp trừu tượng, viết tắt là AST, biểu diễn cấu trúc chương trình. Từ AST có thể lấy khai báo hàm, lớp, lệnh nhập và các tên được tham chiếu. Mở rộng ngữ cảnh theo các tên này giúp bổ sung hàm phụ trợ hoặc giá trị cấu hình liên quan. Giới hạn độ sâu và độ dài là cần thiết để tránh đưa quá nhiều thông tin không phục vụ trực tiếp đối tượng cần kiểm tra.

Thực thi thử thiết lập bổ sung thông tin động cho phân tích tĩnh. Nếu một lời gọi khởi tạo hoặc gọi hàm hoàn tất, có thể dùng chữ ký và đối số của lời gọi làm gợi ý cách sử dụng. Kết quả đó chỉ chứng minh tính khả thi của lời gọi đã thử; không bảo đảm mọi trạng thái phương thức hoặc mọi giá trị đầu vào đều hợp lệ.

## 2.3. Phản hồi thực thi trong sinh và sửa kiểm thử
Phản hồi từ pytest cho biết lỗi xảy ra ở giai đoạn thu thập, chuẩn bị hay thực thi kiểm thử. Dấu vết ngoại lệ và vị trí câu lệnh thất bại giúp mô hình điều chỉnh lời gọi hoặc rà soát điều kiện khẳng định. Sửa lỗi theo phản hồi là một vòng lặp hữu hạn, trong đó bản sửa phải được đánh giá lại trên cùng mã nguồn sản phẩm [3].

Một rủi ro là mô hình làm bộ kiểm thử vượt qua bằng cách xóa hoặc làm yếu điều kiện khẳng định. Kiểm tra cấu trúc có thể phát hiện một số trường hợp như khẳng định hằng đúng, nhưng không chứng minh đầy đủ việc bảo toàn ý nghĩa. Vì vậy, tỷ lệ chạy thành công, khả năng chạy lại và chất lượng điều kiện khẳng định phải được phân tích như các khía cạnh riêng.

## 2.4. Độ phủ, khả năng phát hiện sai lệch và độ ổn định
Tỷ lệ đạt yêu cầu phản ánh khả năng tạo bộ kiểm thử thỏa tiêu chí vận hành đã xác định. Độ phủ câu lệnh, đo theo các dòng có thể thực thi, và độ phủ nhánh phản ánh các phần cấu trúc được thực thi. Trong báo cáo, độ phủ được đo trên mô-đun chứa đối tượng. Đối chứng chuẩn hóa còn yêu cầu có bằng chứng thực thi trong phần thân đối tượng để tránh ghi nhận bộ kiểm thử chỉ chạm tới mã khởi tạo mô-đun.

Kiểm thử đột biến tạo các phiên bản chương trình có thay đổi nhỏ rồi đánh giá xem bộ kiểm thử có nhận biết được sai lệch hay không [7], [13]. Một đột biến được xem là phát hiện khi kiểm thử chạy được trên chương trình gốc nhưng thất bại do điều kiện kiểm tra trên phiên bản biến đổi. Lỗi nhập mô-đun hoặc hết thời gian không được tự động xem là phát hiện lỗi hành vi. Đột biến cũng không đồng nhất với lỗi thực trong phần mềm.

Chạy lại kiểm thử trong tiến trình mới giúp phát hiện một số phụ thuộc trạng thái hoặc môi trường. Nhiều lần chạy lại thành công là bằng chứng ổn định trong điều kiện đã kiểm tra, không phải bảo đảm kiểm thử không bao giờ thay đổi kết quả [16].

## 2.5. Phân tích thống kê theo cấu trúc dự án
Nhiều đối tượng trong cùng dự án có thể chia sẻ quy ước thiết kế và phụ thuộc. Do đó, coi mọi lượt sinh là quan sát độc lập sẽ đánh giá thấp mức bất định. Đề tài lấy trung bình chênh lệch trong từng dự án rồi cân bằng giữa các dự án. Khoảng tin cậy được ước lượng bằng lấy mẫu lại theo cụm dự án; kiểm định đổi dấu cũng được thực hiện ở cấp dự án [9].

Tăng số lần sinh giúp mô tả biến thiên của mô hình trên cùng đối tượng. Tăng số dự án mới hỗ trợ đánh giá khả năng khái quát. Hai thao tác giải quyết hai nguồn bất định khác nhau; không có số lượt gọi cố định nào tự bảo đảm kết luận có ý nghĩa thống kê.

# CHƯƠNG 3. PHƯƠNG PHÁP NGHIÊN CỨU
## 3.1. Phát biểu bài toán và nguyên tắc thiết kế
Đầu vào của bài toán gồm một hàm hoặc lớp Python, mã nguồn mô-đun chứa đối tượng và môi trường thực thi đã xác định. Đầu ra mong muốn là bộ kiểm thử gọi đúng đối tượng, kiểm tra hành vi quan sát được và có thể chạy lại trên cùng phiên bản phần mềm. Ràng buộc của quy trình là số token ngữ cảnh, số token đầu ra và số lượt sửa lỗi hữu hạn.

Phương pháp được thiết kế theo ba nguyên tắc. Thứ nhất, dùng thông tin từ chương trình để giảm suy đoán về giao diện và phụ thuộc. Thứ hai, tách thông tin thiết lập khỏi giá trị mong đợi của kiểm thử. Thứ ba, đánh giá đầu ra bằng thực thi và giữ nguyên các trường hợp không đạt trong mẫu số. Hình 3.1 mô tả mối liên hệ giữa các thành phần.

@figure architecture | Hình 3.1. Quy trình sinh và đánh giá kiểm thử dựa trên ngữ cảnh và phản hồi thực thi

Nguồn: thiết kế của nghiên cứu. Số lượt sửa và các thành phần ngữ cảnh được cố định theo từng cấu hình đánh giá, không mặc định mọi thực nghiệm đều sử dụng đầy đủ các thành phần.

## 3.2. Chuẩn bị ngữ cảnh có giới hạn
Ngữ cảnh cơ sở gồm khai báo đối tượng và các lệnh nhập của mô-đun. Với ví dụ genty, phần bổ sung cần làm rõ quy tắc định dạng và thứ tự đối số khi duyệt, thay vì chỉ nhắc lại các thuộc tính lưu trữ của đối tượng. Ngữ cảnh mở rộng bổ sung khai báo của các tên được đối tượng tham chiếu, chẳng hạn hàm định dạng dữ liệu hoặc hằng số điều khiển hành vi. Phép mở rộng dừng theo độ sâu và ngân sách ký tự đã đặt, giúp giữ trọng tâm của lời nhắc vào chức năng đang kiểm tra.

Ở khảo sát ngữ cảnh phụ trợ sau cùng, việc truy vết chỉ diễn ra trong cùng mô-đun, tối đa hai mức. Mỗi khai báo được giới hạn 4.000 ký tự và tổng phần bổ sung không quá 8.000 ký tự. Đây là một cơ chế mở rộng cục bộ; không đồng nhất với xây dựng đồ thị gọi hàm toàn dự án của Test4Py.

Thông tin thiết lập được tạo bằng cách đọc chữ ký và thử một bộ đối số theo quy tắc chung. Chỉ khi lời gọi hoàn tất, chữ ký và đối số mới được thêm vào ngữ cảnh. Giá trị trả về của lời gọi thử không được cung cấp như kết quả mong đợi. Với lớp, thành công của lời gọi tạo đối tượng chưa chứng minh các phương thức đều có trạng thái hợp lệ.

@algorithm context | Thuật toán 3.1. Chuẩn bị ngữ cảnh mã nguồn và thông tin thiết lập

Giả mã trình bày các bước ở cấp phương pháp. Các thành phần mở rộng được bật hoặc tắt theo thiết kế đối chứng. Ở giai đoạn phát triển ban đầu, hồ sơ giao diện và hướng dẫn thiết lập có một phần do người nghiên cứu chuẩn bị theo thư viện. Hai đợt đánh giá chuẩn hóa sử dụng thông tin thiết lập theo quy tắc chung; khảo sát ngữ cảnh phụ trợ mới bổ sung truy vết khai báo cùng mô-đun. Ba nguồn thông tin này được phân biệt trong phân tích kết quả.

## 3.3. Sinh và sửa kiểm thử bằng phản hồi thực thi
Mô hình nhận lời nhắc gồm yêu cầu nhiệm vụ và ngữ cảnh của đối tượng. Lời nhắc yêu cầu kiểm tra hành vi thông thường, điều kiện biên và ngoại lệ bằng các điều kiện khẳng định cụ thể. Trong đối chứng chuẩn hóa, đầu ra được giới hạn đúng ba hàm kiểm thử nhằm giữ độ lớn nhiệm vụ tương đương giữa hai nhánh.

Bộ kiểm thử được chuẩn hóa định dạng và chạy trên mã nguồn sản phẩm. Nếu không đạt và cấu hình cho phép sửa, thông tin lỗi được gửi lại cùng ngữ cảnh để mô hình đề xuất bản sửa. Số lần sửa tối đa là hai trong các thực nghiệm có phản hồi. Hai vòng dùng cùng loại nhiệm vụ sửa lỗi; không gán một vòng chỉ sửa cú pháp và vòng còn lại chỉ sửa ngữ nghĩa.

@algorithm feedback | Thuật toán 3.2. Sinh và đánh giá kiểm thử với ngân sách sửa lỗi hữu hạn

Hai đợt đối chứng nhiều dự án đặt số lần sửa bằng không để đo riêng hiệu quả của thông tin thiết lập. Kết quả của chúng vì vậy là đánh giá thành phần ngữ cảnh, còn vai trò phản hồi được phân tích từ tập phát triển có sửa lỗi. Cách tách này giúp tránh quy toàn bộ lợi ích của một quy trình kết hợp cho một thành phần riêng lẻ.

Các mẫu lời nhắc được trình bày bằng tiếng Anh tại Phụ lục 1. Báo cáo sử dụng tiếng Việt cho phần lập luận; tên thư viện, lớp và định danh lập trình được giữ nguyên. Lời nhắc trong phụ lục được lấy từ cấu hình đã chạy, không thay đổi ngôn ngữ của dữ liệu thực nghiệm đã lưu.

## 3.4. Tiêu chí đánh giá đầu ra
Đối chứng chuẩn hóa xem một lượt đạt yêu cầu khi bộ kiểm thử đáp ứng kiểm tra cấu trúc, toàn bộ ca kiểm thử vượt qua, độ phủ mô-đun dương, có bằng chứng thực thi phần thân đối tượng và chạy lại cho kết quả độ phủ tương ứng. Các điều kiện này đo khả năng sinh kiểm thử sử dụng được trong quy trình; tính đúng đắn của cơ sở xác định kết quả mong đợi được đánh giá bổ sung bằng xem xét mã nguồn và thay đổi hành vi.

Tỷ lệ đạt yêu cầu được tính bằng số lượt được nhận chia cho toàn bộ lượt dự kiến của nhánh. Độ phủ có tính cả lượt không đạt được tính bằng tổng độ phủ của các lượt đạt chia cho toàn bộ lượt dự kiến; lượt không đạt đóng góp bằng không vào chỉ số tổng hợp này. Quy ước tổng hợp không biến một phép đo bị thiếu thành giá trị độ phủ bằng không. Khi mô-đun không có nhánh cần đo, độ phủ nhánh được ghi là không áp dụng.

Trong kiểm thử đột biến bổ sung, kết quả được chia thành phát hiện, không phát hiện và chưa thể kết luận. Nhóm chưa thể kết luận bao gồm lỗi thu thập, thiết lập hoặc thực thi không đủ điều kiện quy kết cho kiểm tra hành vi. Các nhóm được công bố cùng mẫu số đã lên lịch để tránh tỷ lệ phát hiện tăng do bỏ lỗi thực thi.

## 3.5. Thiết kế thực nghiệm và vai trò của các tập dữ liệu
Thiết kế gồm một đối chứng thành phần chính trên hai tập dự án, một nhóm khảo sát cơ chế và một nghiên cứu ứng dụng. Bảng 3.1 nêu vai trò của từng nguồn bằng chứng. Trong Chương 4, các đợt chạy được tổ chức theo câu hỏi nghiên cứu thay vì theo thứ tự phát sinh tệp kết quả.

@table design | Bảng 3.1. Thiết kế đánh giá và vai trò của các nguồn bằng chứng

Hai tập đối chứng chính sử dụng GPT-OSS-20B, cùng yêu cầu ba hàm kiểm thử, giới hạn 2.048 token đầu ra, nhiệt độ 0,2 và ba giá trị khởi tạo ngẫu nhiên (seed) 42, 43, 44 được gửi qua giao diện lập trình ứng dụng (API). Seed của dịch vụ được xem là cơ chế hỗ trợ lặp lại, không bảo đảm đầu ra mới giống từng byte. Mã nguồn và phiên bản phụ thuộc được cố định theo môi trường đã ghi nhận.

Tập thứ nhất có 27 đối tượng thuộc 9 dự án đủ điều kiện. Tập thứ hai có 34 đối tượng thuộc 12 dự án từ danh sách mô-đun của CodaMOSA [23]. Hai tập không trùng dự án với nhau. Trong tập thứ hai, bốn dự án từng xuất hiện ở giai đoạn phát triển cũ; tám dự án còn lại mở rộng ra ngoài cả tập phát triển đó và các đợt Groq trước. Phiên bản package sử dụng được ghi riêng, vì vậy việc dùng danh sách mô-đun công bố không đồng nghĩa tái lập nguyên phiên bản của benchmark gốc.

Đối tượng được chọn theo điều kiện mã nguồn và thứ tự xác định trước khi sinh kiểm thử. Tập 9 dự án có ba vị trí không được điền do cách nạp mô-đun của black trỏ tới phần mở rộng biên dịch. Tập 12 dự án có hai vị trí không được điền vì codetiming chỉ có một đối tượng đáp ứng tiêu chí. Những vị trí này được công bố trong thiết kế; chúng không bị thay bằng đối tượng có kết quả thuận lợi sau khi chạy mô hình.

## 3.6. Phân tích thống kê và khả năng tái lập
Tương phản chính là tỷ lệ đạt của nhánh bổ sung thiết lập trừ tỷ lệ đạt của nhánh chỉ có mã nguồn. Với mỗi dự án, chênh lệch được tính trên các cặp đối tượng và lượt lặp, sau đó lấy trung bình giữa các dự án. Cách cân bằng này tránh để dự án có nhiều đối tượng chi phối kết quả.

Khoảng tin cậy 95% sử dụng 20.000 lần lấy mẫu lại theo dự án với giá trị khởi tạo cố định. Kiểm định đổi dấu hai phía được tính bằng liệt kê các cách đổi dấu của chênh lệch dự án. Phép kiểm định cần giả định thích hợp về tính độc lập và tính đối xứng của chênh lệch dưới giả thuyết không; việc ghép cặp tự nó không bảo đảm các giả định này. Kế hoạch phân tích của đợt 9 dự án được hoàn thiện sau khi dữ liệu đã thu thập; đợt 12 dự án có kế hoạch trước suy luận nhưng chưa phải đăng ký nghiên cứu bên ngoài.

Mỗi lượt lưu lời nhắc, đầu ra mô hình, mã kiểm thử và kết quả thực thi. Các kiểm thử được nhận còn được chạy lại độc lập. Chạy lại đầu ra đã lưu và tính lại thống kê là hai mức tái lập có thể kiểm tra trực tiếp. Sinh mới qua API là một mức khác, chịu ảnh hưởng của dịch vụ và phiên bản mô hình cung cấp.

# CHƯƠNG 4. THỰC NGHIỆM VÀ ĐÁNH GIÁ
## 4.1. Tổ chức đánh giá theo câu hỏi nghiên cứu
Phần thực nghiệm được tổ chức theo bốn câu hỏi nghiên cứu: hiệu quả trên nhiều dự án, vai trò của các cơ chế cải tiến, chất lượng kiểm thử thu được và tính khả thi vận hành. Các khảo sát nhỏ được dùng để giải thích cơ chế hoặc lựa chọn cấu hình, thay vì trở thành các kết luận độc lập về hiệu quả tổng quát.

Đối chứng chính so sánh mã nguồn với mã nguồn kèm thông tin thiết lập trong cùng điều kiện. Giai đoạn phát triển có thêm hướng dẫn theo thư viện và vòng sửa lỗi, nên được phân tích riêng. Nghiên cứu ứng dụng genty đánh giá giá trị của các kiểm thử 14B đã tạo, không dùng thay cho đối chứng nhiều dự án. Cách tổ chức này thống nhất mục đích đánh giá nhưng vẫn giữ đúng phạm vi của từng mẫu số.

## 4.2. Hiệu quả của thông tin thiết lập trên nhiều dự án
### 4.2.1. Kết quả đối chứng chính
Bảng 4.1 đặt hai tập dự án cạnh nhau để đánh giá khả năng chuyển giao của chính sách cung cấp thiết lập. Mỗi tập vẫn có kết quả và khoảng bất định riêng. Tỷ lệ theo lượt sinh giúp mô tả đầu ra thu được; chênh lệch cân bằng theo dự án là đại lượng dùng cho suy luận chính.

@table primary | Bảng 4.1. Kết quả đối chứng thành phần trên hai tập dự án

Nguồn: kết quả tổng hợp và thống kê của hai đợt đánh giá nhiều dự án. Các khoảng trong bảng là khoảng tin cậy 95% theo cụm dự án, đơn vị điểm phần trăm.

Ở tập 9 dự án, nhánh bổ sung thiết lập ghi nhận 36/81 lượt đạt (44,44%), so với 28/81 (34,57%) ở nhánh mã nguồn. Độ phủ có tính cả lượt không đạt tăng từ 17,36% lên 22,76%. Chênh lệch cân bằng theo dự án là 9,88 điểm phần trăm; khoảng tin cậy từ âm 1,23 đến 22,22 điểm và giá trị p bằng 0,21875. Kết quả ghi nhận tín hiệu cải thiện nhưng chưa đủ bằng chứng xác lập ưu thế thống kê.

Ở tập 12 dự án, tỷ lệ đạt tăng từ 32/102 lên 34/102, tương ứng từ 31,37% lên 33,33%. Độ phủ tăng từ 16,37% lên 18,84%. Chênh lệch cân bằng theo dự án chỉ còn 1,85 điểm phần trăm, với khoảng tin cậy từ âm 6,48 đến 10,19 điểm và giá trị p bằng 0,84375. Chênh lệch cân bằng theo dự án không bằng chênh lệch tỷ lệ gộp theo lượt vì codetiming có ít đối tượng hơn các dự án khác.

@figure effects | Hình 4.1. Chênh lệch tỷ lệ đạt và khoảng tin cậy theo dự án ở hai tập đánh giá

Nguồn: thống kê theo cụm dự án. Mốc không trên trục hoành biểu thị hai nhánh có cùng tỷ lệ đạt; hình không biểu diễn kết quả gộp của hai tập.

### 4.2.2. Diễn giải sự khác biệt giữa các dự án
Hiệu quả không đồng đều giữa các thư viện. Trong tập 12 dự án, sanic ghi nhận 8/9 lượt đạt ở nhánh thiết lập so với 5/9 ở nhánh mã nguồn, còn typesystem giảm từ 2/9 xuống 0/9. cookiecutter và python-string-utils cũng có số lượt đạt thấp hơn một lượt khi thêm thiết lập. Bảng chi tiết theo dự án được trình bày tại Phụ lục 2.

Một nguyên nhân cần xét là thông tin thiết lập chỉ được cung cấp khi lời gọi thử hoàn tất. Trong tập 12 dự án, điều kiện này xảy ra ở 20/34 đối tượng. Với các đối tượng còn lại, hai nhánh không khác nhau về nội dung gợi ý thiết lập. Vì vậy, đối chứng chính đo hiệu quả của chính sách cung cấp thiết lập khi khả thi, không phải hiệu quả của một gợi ý luôn có sẵn và luôn phù hợp.

Phân tích bổ sung trên tám dự án không thuộc tập phát triển lịch sử cho kết quả 19/72 ở nhánh mã nguồn và 24/72 ở nhánh thiết lập. Chênh lệch cân bằng theo dự án là 6,94 điểm phần trăm, với khoảng tin cậy từ âm 2,78 đến 18,06 điểm. Đây là phân tích phạm vi sau thu thập dữ liệu; nó không thay thế tương phản chính trên toàn bộ 12 dự án.

Kết quả trả lời RQ1 theo hướng có điều kiện: thông tin thiết lập có thể hữu ích, nhưng mức cải thiện chưa ổn định giữa các dự án và các khoảng bất định còn rộng. Chưa có cơ sở coi việc thêm thiết lập là cải tiến phổ quát hoặc kết luận vượt toàn bộ phương pháp Test4Py.

## 4.3. Vai trò của ngữ cảnh và phản hồi sửa lỗi
### 4.3.1. Diễn biến kết quả ở giai đoạn phát triển
Trên tập phát triển 21 đối tượng, cấu hình cơ sở đạt 51/105 lượt, cấu hình Council Standard đạt 73/105 lượt và cấu hình ngữ cảnh kết hợp phản hồi đạt 96/105 lượt trước tinh chỉnh. Sau tinh chỉnh trên hai đối tượng đã quan sát, kết quả tổng hợp đạt 98/105 lượt. Bảng 4.2 trình bày đồng thời mốc trước và sau tinh chỉnh để thể hiện quá trình phát triển phương pháp.

@table development | Bảng 4.2. Kết quả phát triển quy trình sinh và sửa kiểm thử

Nguồn: số liệu giai đoạn phát triển đã tổng hợp theo từng cấu hình. Các cấu hình có khác biệt về ngữ cảnh và xử lý phản hồi; kết quả không tách riêng tác động nhân quả của từng thành phần.

Ở cấu hình trước tinh chỉnh, 67 lượt đạt ngay lần sinh đầu và 29 lượt được sửa thành công, gồm 24 lượt ở vòng thứ nhất và 5 lượt ở vòng thứ hai. Sau tinh chỉnh, các số tương ứng là 70 lượt đạt ngay và 28 lượt sửa thành công, gồm 22 lượt ở vòng thứ nhất và 6 lượt ở vòng thứ hai. Phản hồi thực thi giúp khai thác các lần sinh chưa thành công, nhưng thành công sau sửa chưa tự chứng minh mọi điều kiện khẳng định giữ nguyên ý nghĩa.

@figure repair | Hình 4.2. Phân bổ kết quả theo lần sinh và vòng sửa lỗi trên tập phát triển

Nguồn: các mốc đạt đầu tiên trong dữ liệu phát triển. Hai cột biểu diễn cùng quy mô 105 lượt của hai phiên bản tổng hợp; không cộng chúng thành 210 lượt đánh giá độc lập.

Khảo sát loại bỏ thành phần trên sáu đối tượng cho thấy cấu hình đầy đủ đạt 5/6; không dùng phản biện sửa lỗi đạt 4/6; không dùng hướng dẫn giao diện theo thư viện đạt 4/6. Cấu hình không tự động bổ sung lệnh nhập mô-đun đạt 6/6, cao hơn cấu hình đầy đủ trong mẫu nhỏ này. Kết quả cho thấy cần đánh giá cả tác dụng phụ của xử lý bổ sung, thay vì mặc định mọi thành phần đều có lợi. Bảng chi tiết được đưa vào Phụ lục 2.

### 4.3.2. Các khảo sát hỗ trợ lựa chọn ngữ cảnh
Các khảo sát ở Bảng 4.3 được tập hợp trong cùng một mạch phân tích. Khảo sát đầu kiểm tra ngữ cảnh phụ thuộc; các khảo sát sau chuyển trọng tâm sang thiết lập và giới hạn độ lớn của bộ kiểm thử. Chúng phục vụ phát triển cấu hình, không được cộng vào hai đối chứng chính.

@table mechanisms | Bảng 4.3. Khảo sát bổ trợ về ngữ cảnh và thiết lập

Nguồn: kết quả của từng khảo sát. Hai cột số lượt đạt là các đối chứng nội bộ trong cùng hàng; tiêu chí giữa các hàng không hoàn toàn giống nhau.

Trong khảo sát đầu, việc thêm ngữ cảnh phụ thuộc chưa cải thiện kết quả: nhánh mã nguồn đạt 8/27, nhánh bổ sung phụ thuộc đạt 5/27. Kết quả cho thấy có thêm mã nguồn không đồng nghĩa với có ngữ cảnh phù hợp hơn. Ngữ cảnh dài hoặc yêu cầu tạo bộ kiểm thử lớn có thể làm tăng khó khăn về cách sử dụng giao diện và xây dựng điều kiện khẳng định.

Khảo sát tiếp theo dùng ba hàm kiểm thử nhỏ và thông tin thiết lập theo quy tắc chung, đạt 7/18 so với 5/18 của đối chứng. Sau hai đợt đánh giá nhiều dự án, một khảo sát phát triển trên toàn bộ 34 đối tượng đã quan sát tiếp tục bổ sung khai báo phụ trợ cùng mô-đun. Nhánh mã nguồn đạt 11/34 và nhánh ngữ cảnh kết hợp thiết lập đạt 12/34; độ phủ tương ứng là 17,50% và 19,52%. Phần ngữ cảnh phụ trợ thực sự có ở 17/34 đối tượng.

Mức tăng một lượt ở khảo sát sau cùng còn nhỏ. Hơn nữa, ngữ cảnh phụ trợ và thông tin thiết lập được thêm cùng nhau nên chưa tách được đóng góp riêng của truy vết AST. RQ2 vì vậy được trả lời ở mức định hướng: phản hồi thực thi và ngữ cảnh phù hợp hỗ trợ xử lý một số lỗi, nhưng cần đối chứng tách thành phần và phạm vi rộng hơn trước khi khẳng định lợi ích tổng quát.

## 4.4. Chất lượng kiểm thử và nghiên cứu ứng dụng 14B
### 4.4.1. Chạy lại và kiểm tra hành vi đã thực thi
Trong hai tập đối chứng chính, 64 bộ kiểm thử được nhận ở tập 9 dự án và 66 bộ ở tập 12 dự án đều chạy lại thành công, với độ phủ khớp kết quả đã lưu. Khảo sát ngữ cảnh phụ trợ có thêm 23 bộ được nhận và cả 23 bộ cũng chạy lại thành công. Những số liệu này hỗ trợ khả năng tái chạy trong môi trường đã khóa; chúng không phải tỷ lệ ổn định của mọi đầu ra đã sinh.

Phân tích thứ cấp trên khảo sát ban đầu giữ nguyên các ca kiểm thử đã chạy thành công trong bản sinh đầu tiên. Cả hai nhánh phục hồi được bộ không rỗng ở 25/27 lượt dự kiến; số ca giữ lại là 141/208 ở nhánh mã nguồn và 127/216 ở nhánh phụ thuộc. Đây là khả năng tận dụng từng ca kiểm thử, không thay đổi kết quả chính 8/27 và 5/27 của tiêu chí chấp nhận toàn bộ bộ kiểm thử.

Khảo sát đột biến trên tập con này lên lịch 18 lượt đột biến cho mỗi nhánh. Nhánh mã nguồn phát hiện 9, không phát hiện 6 và chưa thể kết luận 3; nhánh phụ thuộc có các số tương ứng là 11, 3 và 4. Phạm vi nhỏ và điều kiện chọn bộ kiểm thử thành công không cho phép diễn giải thành hiệu quả phát hiện lỗi của toàn bộ đầu ra mô hình.

### 4.4.2. Giá trị ứng dụng của kết quả 14B trên genty
Kết quả 14B được sử dụng để xây dựng một bộ kiểm thử ứng dụng cho genty. Bộ ban đầu gồm 12 ca được chọn từ các kiểm thử thật đã sinh, giữ nguyên mã. Bản mở rộng giữ toàn bộ 12 ca và bổ sung hai ca nguyên văn từ một lần sinh 14B khác trong giai đoạn phát triển. Mục đích của nghiên cứu trường hợp là đánh giá giá trị bổ sung của kiểm thử, không ước lượng tỷ lệ thành công trên benchmark.

@table application | Bảng 4.4. Hiệu quả bổ sung kiểm thử trong ứng dụng genty từ kết quả 14B

Nguồn: chạy lại mới trên cùng phiên bản genty và các tệp kiểm thử đã lưu. Mô-đun genty_args không có nhánh được công cụ đo nên chỉ số độ phủ nhánh không áp dụng.

Trường hợp này minh họa khoảng cách giữa kiểm tra trạng thái lưu trữ và kiểm tra hành vi. Các ca cũ kiểm tra thuộc tính args và kwargs nhưng chưa bao phủ đầy đủ phép duyệt. Ca bổ sung kiểm tra cách định dạng đối số vị trí và thứ tự đối số từ khóa khi duyệt. Nhờ đó, độ phủ genty_args tăng từ 18/20 lên 20/20 dòng, trong khi độ phủ genty_repeat được giữ ở 8/8 dòng và 2/2 nhánh.

Hai phiên bản biến đổi hành vi được dùng lại từ hồ sơ phát triển: bỏ định dạng đối số vị trí và đảo thứ tự đối số từ khóa. Bộ 12 ca không phát hiện cả hai; bộ 14 ca phát hiện cả hai bằng lỗi khẳng định. Đây là hai đột biến được chọn sau xem xét kết quả phát triển, không phải hai lỗi thực trong benchmark độc lập. Giá trị của ví dụ nằm ở phần hành vi được kiểm tra thêm và kết quả có thể chạy lại, không phải một tỷ lệ phát hiện lỗi tổng quát bằng 100%.

Bộ mở rộng đạt 14/14 trong ba tiến trình mới. Như vậy, đóng góp ứng dụng của 14B vẫn được giữ trong nghiên cứu dù giai đoạn đánh giá diện rộng chuyển sang Groq. RQ3 ghi nhận bằng chứng tích cực về tái sử dụng và một số kiểm tra hành vi cụ thể; chất lượng điều kiện khẳng định trên toàn bộ benchmark vẫn cần đánh giá bổ sung.

## 4.5. Tính khả thi về tài nguyên và chi phí
### 4.5.1. Từ triển khai 14B đến đánh giá qua API
Sau điều chỉnh attention, cấu hình 14B NF4 hoàn tất bốn phép kiểm tra 4.096 token đầu vào và 512 token đầu ra; bộ nhớ dự trữ cực đại khoảng 10,76 GiB trên GPU được đo. Hai GPU T4 phục vụ các tiến trình riêng. Ở lượt khởi tạo từ đầu, lần sinh đầu tiên xuất hiện sau khoảng 2.627 giây và lượt chạy dừng quanh giới hạn 3.587 giây đã đặt. Bốn lượt mô-đun chưa hoàn tất đánh giá, nên không dùng làm tỷ lệ chất lượng bằng không.

Khi tái sử dụng kết quả của các bước khởi tạo trùng khớp, bốn lượt mô-đun hoàn tất trong khoảng 2.053 giây của tiến trình điều phối. Nhánh cơ sở có 20 ca kiểm thử chạy thành công; nhánh cải tiến không có kiểm thử được ghi nhận theo điều kiện trích xuất và bảo toàn khẳng định của lượt thử. Kết quả này giải thích lựa chọn thay hạ tầng để tiếp tục nghiên cứu, đồng thời cho thấy hạn chế chất lượng cần giữ trong phân tích.

Một đối chứng thành phần khác trên 14B, gồm 12 đối tượng thuộc 4 dự án và 36 lượt mỗi nhánh, cho kết quả chạy thành công và chạy lại là 2/36 với mã nguồn, 4/36 với thông tin API bổ sung. Khi yêu cầu thêm độ phủ Python dương, các số tương ứng là 1/36 và 3/36. Hai tiêu chí được giữ riêng do có trường hợp thực thi qua biên dịch tức thời (Just-In-Time, JIT). Kết quả này là bằng chứng thành phần của giai đoạn 14B, không đối chiếu trực tiếp với các tỷ lệ của Groq.

### 4.5.2. Ngân sách đầu ra và chi phí theo dõi
Khảo sát ngân sách đầu ra được thực hiện trên 27 đối tượng đã quan sát, với hai nhánh ngữ cảnh và một lượt lặp cho mỗi mức giới hạn. Cùng một tiêu chí đánh giá được dùng cho cả hai mức 1.536 và 2.048 token. Bảng 4.5 tóm tắt khảo sát này như một phép lựa chọn cấu hình vận hành.

@table efficiency | Bảng 4.5. Khảo sát hai mức giới hạn token đầu ra

Nguồn: khảo sát vận hành trên tập đã quan sát. Tổng thời gian bao gồm chờ dịch vụ, mạng và chạy kiểm thử; không phải thời gian suy luận thuần của mô hình.

Không câu trả lời nào chạm giới hạn đầu ra. Mức 1.536 token đạt 22/54 lượt và sử dụng 26.821 token đầu ra; mức 2.048 đạt 24/54 và dùng 25.439 token. Trong khảo sát này, hạ giới hạn không làm giảm số token thực tế. Nghiên cứu giữ mức 2.048 như khoảng dự phòng vận hành, không xem đây là bằng chứng đã tìm được mức tối ưu.

Sổ theo dõi API ghi 688 phản hồi có thông tin sử dụng, với chi phí ước tính theo đơn giá cấu hình là 0,158223 USD. Tổng phân bổ bảo thủ là 0,605180 USD, gồm các khoản đặt trước và đối soát mốc ban đầu, nằm trong trần 3 USD. Hai số liệu phục vụ hai mục đích và không được cộng thành chi phí thực trả. Số phản hồi trong sổ theo dõi không phải cỡ mẫu thống kê của một đối chứng. Các phản hồi có sử dụng được ghi nhận với trạng thái HTTP 200; lịch gọi được điều tiết theo hạn mức dịch vụ.

RQ4 cho thấy đánh giá thành phần qua API khả thi trong ngân sách đã theo dõi, còn triển khai 14B tại chỗ chịu ảnh hưởng lớn của khởi tạo và thời lượng thực thi. Thời gian chạy lại bộ kiểm thử trên CPU không được dùng để so tốc độ sinh của hai mô hình. Kết quả 14B được đánh giá thêm theo giá trị kiểm thử tái sử dụng thay vì chỉ theo tốc độ hạ tầng.

## 4.6. Tổng hợp kết quả và giới hạn nghiên cứu
Các kết quả nhất quán ở một điểm: kiểm thử sử dụng được cần nhiều hơn khả năng sinh cú pháp đúng. Thông tin giao diện, trạng thái đầu vào và phản hồi thực thi có thể hỗ trợ mô hình, nhưng lợi ích phụ thuộc thư viện và cách lựa chọn ngữ cảnh. Hai đối chứng nhiều dự án đều có chênh lệch dương về mặt mô tả, song khoảng tin cậy còn chứa không. Kết luận phù hợp là hướng tiếp cận có tiềm năng phát triển, chưa xác lập cải tiến ổn định trên phạm vi rộng.

Về tính hợp lệ của phép đo, chạy thành công và độ phủ không thay thế cơ sở xác định kết quả mong đợi. Chạy lại xác nhận sự nhất quán trong môi trường được kiểm tra; khảo sát đột biến nhỏ chỉ kiểm tra một phần độ nhạy hành vi. Bộ đột biến 187 trường hợp ở giai đoạn cũ sử dụng các bộ kiểm thử chuẩn tuyển chọn và cách quy kết khác, nên được lưu tại phụ lục thay vì dùng làm kết quả phát hiện lỗi của phương pháp đang đối chứng.

Về tính hợp lệ nội tại, tập phát triển ban đầu có hướng dẫn theo thư viện và tinh chỉnh trên đối tượng đã quan sát. Một số hướng dẫn có ví dụ điều kiện khẳng định, nên kết quả này không được dùng làm bằng chứng về khả năng tự xây dựng kết quả mong đợi trên dữ liệu mới. Việc làm yếu khẳng định khi sửa lỗi chưa được loại trừ bằng kiểm tra ngữ nghĩa đầy đủ. Các hồ sơ thiếu chi tiết và sai khác của giai đoạn này được ghi tại phụ lục. Các hạn chế đó không được đưa vào mô tả phương pháp như những bảo đảm tự động đã có.

Về kết luận thống kê, 9 và 12 cụm dự án còn cho khoảng bất định rộng. Các lần sinh lặp lại không bổ sung số dự án độc lập. Về khả năng khái quát, các thư viện chủ yếu được chọn theo điều kiện thực thi Python và nguồn mã sẵn có; một phần dự án đã dùng trước đó. Phiên bản package thích nghi cũng khác với bản gốc của benchmark. Vì vậy, nghiên cứu không khẳng định vượt Test4Py dựa trên việc so tỷ lệ cục bộ với số tổng hợp của bài báo.

## 4.7. Mở rộng đánh giá toàn bộ phạm vi benchmark
Đánh giá toàn bộ phạm vi đủ điều kiện sẽ thuyết phục hơn việc chỉ giữ vài trường hợp minh họa khi mục tiêu là mô tả hiệu quả trên benchmark. Nghiên cứu trường hợp vẫn cần để giải thích cơ chế, nhưng không nên thay thế đối chứng diện rộng. Cần xác định rõ “toàn bộ” là toàn bộ mô-đun của benchmark công bố, hay toàn bộ đối tượng đủ điều kiện trong một tập thích nghi đã xác định.

Các danh mục mã nguồn đã lưu của hai tập đối chứng hiện có 645 hàm hoặc lớp đủ tiêu chí trên 169 mô-đun thuộc 21 dự án. Hai đợt đối chứng mới dùng 61 đối tượng trong phạm vi đó. Nếu dùng toàn bộ 645 đối tượng, hai nhánh và ba lượt lặp trong đối chứng thành phần không sửa lỗi, thiết kế sẽ có 3.870 lượt sinh. Đây là quy mô dự kiến từ danh mục, chưa phải số lượt đã chạy và chưa phải toàn bộ benchmark Test4Py gốc.

Thiết kế tiếp theo nên cố định phiên bản benchmark, điều kiện đủ tiêu chí và danh sách đối tượng trước khi sinh; công bố số lượng từ danh mục ban đầu đến đủ điều kiện, hoàn tất và không hoàn tất. Mọi đối tượng đủ điều kiện đều được đánh giá, kể cả trường hợp không sinh được mã hoặc không vượt qua kiểm thử. Ngân sách, số lần sửa và tiêu chí nhận phải tương đương giữa các nhánh. Phân tích tiếp tục ghép cặp và cân bằng theo dự án.

Chạy thêm nhiều đối tượng trong 21 dự án đã quan sát làm rõ hiệu quả trong phạm vi này nhưng không tạo ra dự án độc lập mới. Để xác nhận khả năng khái quát, nên bổ sung dự án chưa dùng trong phát triển. Nếu mục tiêu là khẳng định vượt Test4Py, cần chạy cả quy trình đề xuất và Test4Py trên cùng phiên bản phần mềm, phạm vi đầu vào và ngân sách. Nếu mục tiêu là phát hiện lỗi thật, có thể thiết kế đánh giá riêng trên cặp phiên bản lỗi và đã sửa của BugsInPy [24], với bộ kiểm thử chuẩn được giữ ngoài lời nhắc.

Kinh phí và thời gian của lượt chạy toàn bộ cần được tính từ độ dài lời nhắc thực tế và hạn mức dịch vụ. Không suy từ số tiền còn lại rằng mọi thiết kế toàn bộ đều chắc chắn hoàn thành trong trần 3 USD. Việc tăng quy mô phải phục vụ câu hỏi nghiên cứu đã khóa, không nhằm tìm một tập con có kết quả thuận lợi hoặc bảo đảm trước một giá trị p.

# CHƯƠNG 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
## 5.1. Kết luận theo câu hỏi nghiên cứu
Đề tài đã triển khai quy trình sinh và sửa kiểm thử Python dựa trên ngữ cảnh mã nguồn, thông tin thiết lập và phản hồi thực thi. Nội dung cải tiến nằm ở việc làm rõ giao diện sử dụng và tập trung ngữ cảnh liên quan trong ngân sách nhỏ. Kết quả được đánh giá qua đối chứng thành phần, phân tích quá trình phát triển và một ứng dụng có kiểm thử tái sử dụng.

@table conclusions | Bảng 5.1. Tổng hợp câu trả lời cho bốn câu hỏi nghiên cứu

Hai đối chứng nhiều dự án cho thấy mức tăng quan sát của chính sách thiết lập lần lượt là 9,88 và 1,85 điểm phần trăm khi cân bằng theo dự án. Khoảng tin cậy của cả hai còn chứa không. Dữ liệu chưa đủ để xác nhận ưu thế thống kê hoặc vượt phương pháp Test4Py đầy đủ.

Giá trị ứng dụng cụ thể được ghi nhận từ giai đoạn 14B: bộ 14 ca giữ nguyên 12 ca cũ, tăng độ phủ genty_args từ 18/20 lên 20/20 dòng và phát hiện hai biến đổi hành vi mà bộ cũ bỏ sót. Kết quả này cho thấy có thể tái sử dụng kiểm thử sinh thật, đồng thời nhấn mạnh sự khác biệt giữa cải thiện một bộ kiểm thử cụ thể và chứng minh hiệu quả tổng quát của thuật toán.

## 5.2. Hướng phát triển
Hướng ưu tiên là đánh giá toàn bộ đối tượng đủ điều kiện trong một khung benchmark cố định, đồng thời bổ sung dự án độc lập để kiểm tra khả năng chuyển giao. Trong thiết kế thành phần, cần tách ngữ cảnh phụ trợ, thiết lập và sửa lỗi thành các nhánh đối chứng có ngân sách tương đương. Với đánh giá toàn quy trình, cần đối chứng trực tiếp với Test4Py thay vì so các số tổng hợp khác phạm vi.

Nghiên cứu tiếp theo cũng cần tăng chất lượng thông tin thiết lập, rà soát cơ sở xác định kết quả mong đợi và dùng lỗi thực hoặc tập đột biến được chọn trước. Các thay đổi này nhằm chuyển từ tín hiệu cải thiện trong thực nghiệm thăm dò sang bằng chứng có độ tin cậy và phạm vi khái quát rõ ràng hơn.
