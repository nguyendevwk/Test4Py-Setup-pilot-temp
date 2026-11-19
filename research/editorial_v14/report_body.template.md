# MỞ ĐẦU
## 1. Lý do chọn đề tài
Kiểm thử đơn vị giúp phát hiện thay đổi ngoài ý muốn khi phần mềm được sửa đổi. Với Python, một ca kiểm thử có ích phải đồng thời gọi đúng giao diện, tạo được trạng thái đầu vào hợp lệ và kiểm tra kết quả có ý nghĩa. Mô hình ngôn ngữ lớn có thể hỗ trợ viết mã kiểm thử, nhưng việc chỉ cung cấp phần thân hàm thường chưa đủ để đáp ứng ba yêu cầu này. Các thông tin quan trọng có thể nằm trong hàm phụ trợ, cấu trúc đối tượng hoặc quy ước sử dụng của thư viện.

Một ví dụ cụ thể là lớp GentyArgs của thư viện genty. Kiểm tra các thuộc tính lưu đối số chưa bao quát hành vi duyệt đối số. Muốn kiểm tra hành vi đó, bộ kiểm thử cần biết quy tắc định dạng giá trị và thứ tự của đối số từ khóa. Một bộ kiểm thử có thể chạy thành công nhưng vẫn bỏ sót sai lệch ở phần hành vi chưa được kiểm tra. Bài toán nghiên cứu vì vậy không chỉ là tạo mã chạy được, mà là cung cấp đủ ngữ cảnh để sinh được kiểm thử thực thi đúng và có khả năng nhận biết thay đổi hành vi.

Test4Py giải quyết khó khăn về đầu vào cho Python bằng đồ thị gọi hàm, suy luận kiểu dựa trên hành vi và quy trình sửa kiểm thử lặp [1]. Trên cơ sở bài toán đó, đề tài khảo sát một hướng tiếp cận gọn hơn: kết hợp ngữ cảnh mã nguồn có giới hạn, thông tin thiết lập đã được thực thi thử và phản hồi từ môi trường kiểm thử. Hướng tiếp cận được gọi là Council trong báo cáo. Tên gọi này chỉ quy trình sinh và phản biện kiểm thử, không hàm ý đã đạt kết quả tốt nhất hiện có.

## 2. Mục tiêu và câu hỏi nghiên cứu
Mục tiêu của đề tài là xây dựng và đánh giá quy trình hỗ trợ sinh, sửa kiểm thử đơn vị cho các hàm và lớp Python trong điều kiện tài nguyên suy luận hạn chế. Nghiên cứu tập trung vào bốn câu hỏi nghiên cứu (research question, viết tắt RQ) sau.

RQ1. Ngữ cảnh có giới hạn kết hợp thông tin thiết lập đã được thực thi thử có cải thiện tỷ lệ bộ kiểm thử đạt yêu cầu và độ phủ so với chỉ cung cấp mã nguồn trên nhiều dự án hay không?

RQ2. Thông tin thiết lập, khai báo phụ trợ và phản hồi thực thi đóng góp như thế nào vào quá trình sinh và sửa kiểm thử?

RQ3. Các kiểm thử thu được có chạy lại ổn định và phát hiện được thay đổi hành vi trong phạm vi đánh giá hay không?

RQ4. Quy trình có khả thi về tài nguyên, chi phí suy luận và khả năng tái sử dụng kết quả hay không?

## 3. Đối tượng và phạm vi nghiên cứu
Đối tượng nghiên cứu là bộ kiểm thử do mô hình ngôn ngữ sinh cho các hàm và lớp thuộc thư viện Python công khai. Nguồn đối tượng được xác định từ các bộ chuẩn đánh giá (benchmark) và danh mục mô-đun liên quan. Đánh giá trọng tâm bao phủ toàn bộ 645 đối tượng đủ điều kiện trên 169 mô-đun thuộc 21 dự án trong danh mục hiện có. Ba cấu hình ngữ cảnh và hai lượt lặp tạo 3.870 lượt đánh giá. Giai đoạn phát triển trên 21 đối tượng, hai đợt đối chứng nhỏ hơn và các khảo sát vận hành được giữ làm bằng chứng bổ trợ. Các đợt có thiết kế khác nhau được dùng để trả lời các khía cạnh tương ứng của cùng bài toán, không cộng thành một mẫu thống kê đồng nhất.

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

## 3.5. Thiết kế thực nghiệm trên toàn bộ phạm vi đủ điều kiện
Đánh giá chính sử dụng toàn bộ 645 hàm hoặc lớp đáp ứng tiêu chí nguồn mã trong các danh mục đã lưu. Các đối tượng thuộc 169 mô-đun và 21 dự án; không chỉ giữ vài trường hợp đại diện. Danh sách, phiên bản môi trường, lời nhắc, số lượt lặp và kế hoạch phân tích được cố định trước khi gọi mô hình cho đợt này.

Ba nhánh được so sánh ghép cặp gồm chỉ mã nguồn, mã nguồn kèm thiết lập đã thử, và mã nguồn kèm cả thiết lập lẫn khai báo phụ trợ. Mỗi đối tượng có hai lượt lặp, với giá trị seed 71 và 72 được gửi qua API. Cả ba nhánh sử dụng GPT-OSS-20B, nhiệt độ 0,2, giới hạn 2.048 token đầu ra và không sửa lỗi, tạo tổng cộng 3.870 lượt, tương ứng 1.290 lượt mỗi nhánh. Việc ưu tiên ba cấu hình giúp đánh giá đóng góp thành phần trên cùng tập đối tượng; số lượt lặp không thay thế số dự án độc lập.

@table design | Bảng 3.1. Thiết kế đánh giá chính và các nguồn bằng chứng bổ trợ

Tập đối tượng gồm 357 hàm và 288 lớp. Độ dài khai báo trung vị là 22 dòng, với khoảng tứ phân vị từ 12 đến 42 dòng; tiêu chí chọn nguồn mã vì vậy cần được xét khi khái quát tới các lớp lớn hơn hoặc hệ thống tích hợp.

Thông tin thiết lập dùng được ở 337/645 đối tượng; phần khai báo phụ trợ có ở 388/645 đối tượng. Khi không có một loại thông tin bổ sung, đối tượng vẫn được giữ trong mẫu đánh giá và nhánh tương ứng dùng phần ngữ cảnh còn lại. Tương phản vì vậy đo hiệu quả của một chính sách bổ sung thông tin khi có thể thu được, không giả định mọi đối tượng đều có gợi ý hoàn hảo.

Điều kiện đủ tiêu chí được xác định từ nguồn mã trước suy luận: khai báo công khai ở cấp mô-đun, dài từ 5 đến 160 dòng và phần khai báo đối tượng không quá 6.000 ký tự. Các mô-đun được lấy theo danh mục liên quan tới Test4Py và CodaMOSA [1], [23], với phiên bản package được khóa theo môi trường đã ghi nhận. Việc phủ toàn bộ danh mục đủ điều kiện này không đồng nghĩa tái lập nguyên phiên bản hoặc toàn bộ mô-đun của hai benchmark gốc.

Các nhánh chạy luân phiên trong từng cặp đối tượng và lượt lặp. Cơ chế thu thập được tăng từ HTTP tuần tự lên tối đa tám yêu cầu đồng thời theo yêu cầu điều phối, trong trần 1.000 yêu cầu và 250.000 token mỗi phút. Các tham số sinh, đối tượng và tiêu chí đánh giá giữ nguyên; giai đoạn điều phối được ghi riêng khi diễn giải thời gian và tài nguyên. Kiểm thử được thực thi trong tiến trình riêng, dùng môi trường phụ thuộc của dự án và cùng giới hạn thời gian 20 giây mỗi lần chạy. Đầu ra phải có đúng ba hàm kiểm thử cấp mô-đun; cả ba hàm phải được pytest thu thập và chạy thành công. Các trường hợp tham số hóa được tính là các ca trong ba hàm này, không phải đối tượng thống kê mới.

Trong 645 đối tượng, 61 đã được dùng ở hai đợt đối chứng chuẩn hóa trước, còn 584 chưa nằm trong hai tập đối chứng đó. Tuy nhiên, cả 21 dự án đều đã được quan sát trong quá trình triển khai. Đợt này đánh giá độ bao quát trong khung đã xác định, không được gọi là xác nhận trên 21 dự án hoàn toàn mới. Các số liệu cũ không được cộng vào 3.870 lượt của đối chứng chính.

## 3.6. Phân tích thống kê và khả năng tái lập
Tương phản chính đã khóa là nhánh ngữ cảnh kết hợp thiết lập trừ nhánh chỉ mã nguồn. Hai tương phản phụ là thiết lập trừ mã nguồn và ngữ cảnh kết hợp trừ thiết lập. Tương phản phụ thứ hai đo phần giá trị bổ sung của khai báo phụ trợ khi giữ cùng chính sách thiết lập.

Với mỗi dự án, chênh lệch được tính trên các cặp đối tượng và lượt lặp, sau đó lấy trung bình giữa các dự án. Báo cáo đồng thời trình bày tỷ lệ theo lượt để mô tả số bộ kiểm thử sử dụng được và tỷ lệ cân bằng dự án để phân tích khả năng chuyển giao. Độ phủ có tính lượt không đạt cũng được báo theo cùng cách cân bằng khi dùng cho đánh giá chính.

Khoảng tin cậy 95% sử dụng 20.000 lần lấy mẫu lại theo cụm dự án, với giá trị khởi tạo 20261119. Kiểm định đổi dấu hai phía được tính ở cấp 21 dự án. Phép kiểm định cần giả định độc lập và khả năng hoán đổi dấu của chênh lệch dưới giả thuyết không; việc ghép cặp tự nó không bảo đảm các giả định này. Hai giá trị p của các tương phản phụ được hiệu chỉnh bằng phương pháp Holm; tương phản chính được xác định riêng trước chạy. Các khoảng tin cậy là khoảng biên cho từng tương phản, không phải khoảng đồng thời.

Phân tích kết luận chỉ được thực hiện khi có đủ toàn bộ tích các đối tượng, ba nhánh và hai lượt lặp. Không dừng nghiên cứu khi thấy kết quả thuận lợi. Mọi đầu ra mô hình không đạt tiêu chí vẫn nằm trong mẫu số. Sự cố truyền thông, bằng chứng hỏng hoặc nguồn mã bị thay đổi làm tạm dừng để đối chiếu, không bị chuyển thành một kết quả chất lượng mô hình đã quan sát.

Mỗi lượt lưu lời nhắc, đầu ra mô hình, mã kiểm thử và kết quả thực thi. Các bộ được nhận còn được chạy lại độc lập. Chạy lại đầu ra đã lưu và tính lại thống kê là hai mức tái lập có thể kiểm tra trực tiếp. Sinh mới qua API là một mức khác, chịu ảnh hưởng của dịch vụ và phiên bản mô hình cung cấp.

# CHƯƠNG 4. THỰC NGHIỆM VÀ ĐÁNH GIÁ
## 4.1. Tổ chức đánh giá theo câu hỏi nghiên cứu
Phần thực nghiệm lấy đợt bao phủ toàn bộ danh mục đủ điều kiện làm kết quả trung tâm. Đợt này hoàn tất {{COMPLETED}} trên 3.870 lượt dự kiến, bao gồm cả các lượt không sinh được mã hợp lệ hoặc không vượt qua kiểm thử. Các bằng chứng phát triển, vòng sửa lỗi và ứng dụng 14B được dùng để giải thích cơ chế và giá trị sử dụng, thay vì trở thành những thực nghiệm nhỏ tách rời.

RQ1 được trả lời bằng tương phản chính giữa ngữ cảnh kết hợp và mã nguồn. RQ2 được phân tích qua hai tương phản thành phần trên cùng tập, cùng bằng chứng phản hồi ở giai đoạn phát triển. RQ3 sử dụng chạy lại và kiểm tra thay đổi hành vi; RQ4 đánh giá tài nguyên và ngân sách. Các kết quả cũ giữ mẫu số riêng và được đặt trong tiến trình phát triển phương pháp.

## 4.2. Kết quả trên toàn bộ 645 đối tượng đủ điều kiện
### 4.2.1. Khả năng tạo bộ kiểm thử sử dụng được
Bảng 4.1 trình bày ba cấu hình trên cùng 645 đối tượng thuộc 21 dự án. Số lượt đạt theo mẫu số 1.290 mô tả sản phẩm kiểm thử thu được. Tỷ lệ và độ phủ cân bằng dự án tránh để các thư viện có nhiều đối tượng chi phối kết luận.

@table primary | Bảng 4.1. Kết quả ba cấu hình trên toàn bộ danh mục đủ điều kiện

Nguồn: kết quả đầy đủ của đợt đánh giá 3.870 lượt. Độ phủ được đo trên mô-đun, tính cả các lượt không đạt theo quy ước của mục 3.4.

Nhánh chỉ mã nguồn đạt {{SOURCE_K}}/1.290 lượt ({{SOURCE_PR}}%). Nhánh thêm thiết lập đạt {{SETUP_K}}/1.290 lượt ({{SETUP_PR}}%), còn nhánh ngữ cảnh kết hợp đạt {{CONTEXT_K}}/1.290 lượt ({{CONTEXT_PR}}%). Tỷ lệ cân bằng dự án tương ứng là {{SOURCE_EQ}}%, {{SETUP_EQ}}% và {{CONTEXT_EQ}}%. Chênh lệch cân bằng dự án có thể khác chênh lệch tỷ lệ theo lượt do quy mô đối tượng giữa các dự án không bằng nhau.

### 4.2.2. Hiệu ứng phương pháp và đóng góp thành phần
@table contrasts | Bảng 4.2. Chênh lệch ghép cặp và mức bất định theo dự án

Nguồn: phân tích theo kế hoạch đã khóa. Chênh lệch và khoảng tin cậy dùng đơn vị điểm phần trăm. Hiệu chỉnh Holm áp dụng cho hai tương phản phụ; độ phủ là chỉ số mô tả.

Tương phản chính giữa ngữ cảnh kết hợp và mã nguồn là {{PRIMARY_DIFF}} điểm phần trăm, với khoảng tin cậy 95% từ {{PRIMARY_LO}} đến {{PRIMARY_HI}} điểm và p hai phía bằng {{PRIMARY_P}}. {{PRIMARY_INTERPRETATION}}

Tương phản thiết lập so với mã nguồn là {{SETUP_DIFF}} điểm phần trăm, với p đã hiệu chỉnh {{SETUP_HOLM}}. Khi giữ cùng thông tin thiết lập và bổ sung khai báo phụ trợ, chênh lệch là {{CLOSURE_DIFF}} điểm phần trăm, với p đã hiệu chỉnh {{CLOSURE_HOLM}}. Hai kết quả này giúp phân biệt phần giá trị của thiết lập với phần giá trị của khai báo phụ trợ, thay vì quy toàn bộ kết quả cho AST. Tương phản bổ sung khai báo có khoảng bootstrap dương nhưng chưa đạt ngưỡng 0,05 theo kiểm định đổi dấu và hiệu chỉnh Holm; không dùng riêng khoảng này để khẳng định ưu thế.

@figure effects | Hình 4.1. Hiệu ứng của phương pháp và hai tương phản thành phần theo dự án

Nguồn: phân tích cụm của đợt đánh giá đầy đủ. Mốc không trên trục hoành biểu thị hai nhánh có cùng tỷ lệ đạt. Các khoảng là khoảng tin cậy biên 95%.

Phân bố kết quả của toàn bộ 21 dự án được trình bày tại Phụ lục 2. Kết quả có thể khác nhau theo kiểu giao diện và mức thông tin bổ sung thu được; số đối tượng lớn không làm các dự án trở thành mẫu ngẫu nhiên của mọi phần mềm Python. Đợt toàn phạm vi làm rõ mức độ bao quát trong khung đã cố định, còn khả năng khái quát ra các dự án mới vẫn cần đánh giá riêng.

RQ1 được trả lời theo phạm vi tương phản chính và khoảng bất định đã báo. RQ2 về đóng góp thiết lập và khai báo phụ trợ được đánh giá bằng hai tương phản phụ cùng dữ liệu, thay vì chọn một tập con có kết quả tốt hơn.

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

## 4.4. Chất lượng kiểm thử và nghiên cứu ứng dụng 14B
### 4.4.1. Chạy lại và kiểm tra hành vi đã thực thi
Trong đợt toàn phạm vi, có {{ACCEPTED_TOTAL}} bộ được nhận theo tiêu chí thực thi và chạy lại của quy trình. Kiểm tra độc lập tiếp theo chạy lại {{REPLAY_COUNT}} bộ: {{REPLAY_PASSED}} bộ vượt qua và {{REPLAY_MATCHED}} bộ khớp độ phủ đã lưu. {{REPLAY_INTERPRETATION}} Hai đợt đối chứng trước có 64 và 66 bộ được nhận đều chạy lại thành công; khảo sát phụ trợ cũ có thêm 23 bộ với cùng kết quả kiểm tra. Những số liệu này hỗ trợ khả năng tái chạy trong môi trường đã khóa; chúng không phải tỷ lệ ổn định của mọi đầu ra đã sinh.

Khả năng ghép các bộ được nhận thành gói chạy chung được khảo sát bổ sung trên toàn bộ 21 dự án và ba nhánh. Tất cả mã kiểm thử được giữ nguyên; mỗi dự án và nhánh tạo một gói, gồm cả hai lượt lặp. Số gói vượt qua toàn bộ kiểm thử lần lượt là {{SOURCE_PACKS}}/21, {{SETUP_PACKS}}/21 và {{CONTEXT_PACKS}}/21. Độ phủ trung bình của gói hợp lệ trên toàn bộ 21 dự án tương ứng là {{SOURCE_PACK_COVERAGE}}%, {{SETUP_PACK_COVERAGE}}% và {{CONTEXT_PACK_COVERAGE}}%; gói không đạt đóng góp bằng không vào chỉ số tổng hợp. Độ phủ chưa đo được vẫn giữ là không có dữ liệu ở hồ sơ gốc. Đây là đánh giá khả năng tích hợp, được bổ sung khi đang thu thập dữ liệu, không thay thế kết quả chính hoặc kiểm định đã khóa.

Phân tích thứ cấp trên khảo sát ban đầu giữ nguyên các ca kiểm thử đã chạy thành công trong bản sinh đầu tiên. Cả hai nhánh phục hồi được bộ không rỗng ở 25/27 lượt dự kiến; số ca giữ lại là 141/208 ở nhánh mã nguồn và 127/216 ở nhánh phụ thuộc. Đây là khả năng tận dụng từng ca kiểm thử, không thay đổi kết quả chính 8/27 và 5/27 của tiêu chí chấp nhận toàn bộ bộ kiểm thử.

Khảo sát đột biến trên tập con này lên lịch 18 lượt đột biến cho mỗi nhánh. Nhánh mã nguồn phát hiện 9, không phát hiện 6 và chưa thể kết luận 3; nhánh phụ thuộc có các số tương ứng là 11, 3 và 4. Phạm vi nhỏ và điều kiện chọn bộ kiểm thử thành công không cho phép diễn giải thành hiệu quả phát hiện lỗi của toàn bộ đầu ra mô hình.

### 4.4.2. Giá trị ứng dụng của kết quả 14B trên genty
Kết quả 14B được sử dụng để xây dựng một bộ kiểm thử ứng dụng cho genty. Bộ ban đầu gồm 12 ca được chọn từ các kiểm thử thật đã sinh, giữ nguyên mã. Bản mở rộng giữ toàn bộ 12 ca và bổ sung hai ca nguyên văn từ một lần sinh 14B khác trong giai đoạn phát triển. Mục đích của nghiên cứu trường hợp là đánh giá giá trị bổ sung của kiểm thử, không ước lượng tỷ lệ thành công trên benchmark.

@table application | Bảng 4.5. Hiệu quả bổ sung kiểm thử trong ứng dụng genty từ kết quả 14B

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
Bảng 4.6 so sánh lượng token và chi phí sử dụng ước tính của ba nhánh trong cùng đợt toàn phạm vi. Tổng chi phí theo nhánh dùng tất cả lượt sinh của nhánh, gồm cả lượt không đạt. Chi phí trên mỗi bộ đạt được tính bằng tổng ước tính chia cho số bộ được nhận; chỉ số này mô tả đánh đổi vận hành trong phạm vi đã đo.

@table efficiency | Bảng 4.6. Token và chi phí sử dụng ước tính của ba nhánh

Nguồn: trường usage trong các phản hồi đã lưu; ước tính theo đơn giá cấu hình 0,075 USD mỗi triệu token đầu vào và 0,30 USD mỗi triệu token đầu ra. Đây không phải hóa đơn; giá đầu vào có bộ nhớ đệm có thể thấp hơn mức cấu hình bảo thủ.

Khảo sát lựa chọn cấu hình trước đó trên 27 đối tượng đã quan sát dùng hai giới hạn 1.536 và 2.048 token, tổng 108 lượt. Không câu trả lời nào chạm giới hạn. Mức 1.536 token đạt 22/54 lượt và sử dụng 26.821 token đầu ra; mức 2.048 đạt 24/54 và dùng 25.439 token. Trong khảo sát này, hạ giới hạn không làm giảm số token thực tế. Nghiên cứu giữ mức 2.048 như khoảng dự phòng vận hành, không xem đây là bằng chứng đã tìm được mức tối ưu.

Sau đợt toàn phạm vi, sổ theo dõi API ghi {{SETTLED_RESPONSES}} phản hồi có thông tin sử dụng, với chi phí ước tính theo đơn giá cấu hình là {{SETTLED_COST}} USD. Tổng phân bổ bảo thủ là {{ACCOUNTED_COST}} USD, gồm các khoản đặt trước và đối soát mốc ban đầu, nằm trong trần 3 USD. Riêng đợt toàn phạm vi có chi phí sử dụng ước tính {{FULL_COST}} USD. Hai số liệu phục vụ hai mục đích và không được cộng thành chi phí thực trả. Số phản hồi trong sổ theo dõi không phải cỡ mẫu thống kê của một đối chứng. Lịch gọi được điều tiết theo hạn mức dịch vụ; mọi sự cố và khoản đặt trước chưa quyết toán được giữ trong sổ theo dõi.

RQ4 cho thấy đánh giá thành phần qua API khả thi trong ngân sách đã theo dõi, còn triển khai 14B tại chỗ chịu ảnh hưởng lớn của khởi tạo và thời lượng thực thi. Thời gian chạy lại bộ kiểm thử trên CPU không được dùng để so tốc độ sinh của hai mô hình. Kết quả 14B được đánh giá thêm theo giá trị kiểm thử tái sử dụng thay vì chỉ theo tốc độ hạ tầng.

## 4.6. Tổng hợp kết quả và giới hạn nghiên cứu
Đợt toàn phạm vi mở rộng bằng chứng từ vài đối tượng được chọn sang toàn bộ 645 đối tượng đủ điều kiện trong danh mục. Ba nhánh và hai lượt lặp được áp dụng theo cùng một thiết kế trên 21 dự án, giúp đánh giá phương pháp và thành phần trong một mạch thống nhất. {{PRIMARY_INTERPRETATION}} Phạm vi kết luận vẫn là chính sách cung cấp ngữ cảnh trong môi trường và tiêu chí đã xác định, không phải ưu thế so với toàn bộ Test4Py.

Về tính hợp lệ của phép đo, chạy thành công và độ phủ không thay thế cơ sở xác định kết quả mong đợi. Chạy lại xác nhận sự nhất quán trong môi trường được kiểm tra; khảo sát đột biến nhỏ chỉ kiểm tra một phần độ nhạy hành vi. Các khảo sát đột biến lịch sử sử dụng bộ kiểm thử tuyển chọn nên được phân biệt với kết quả sinh kiểm thử của đợt toàn phạm vi.

Về tính hợp lệ nội tại, quy tắc ngữ cảnh và phân tích của đợt mới được khóa trước suy luận. Tuy nhiên, các dự án đã được quan sát và 61 đối tượng từng tham gia đối chứng trước. Giai đoạn phát triển cũ còn có hướng dẫn theo thư viện, ví dụ điều kiện khẳng định và tinh chỉnh trên đối tượng đã quan sát. Nghiên cứu giữ các bằng chứng phát triển này riêng, không coi là xác nhận khả năng tự xây dựng kết quả mong đợi trên dự án chưa biết.

Về kết luận thống kê, số lượt tăng lên 3.870 không tạo ra 3.870 dự án độc lập. Phân tích vẫn dựa trên 21 cụm dự án với các giả định đã nêu. Các thư viện công khai cũng có thể đã xuất hiện trong dữ liệu tiền huấn luyện của mô hình. Phiên bản package và phạm vi đủ tiêu chí khác benchmark gốc. Chưa có đối chứng toàn quy trình với Test4Py trên cùng điều kiện; độ phủ cao hoặc một tương phản có ý nghĩa thống kê không tự cung cấp đối chứng đó.

## 4.7. Phạm vi đã bao phủ và hướng mở rộng benchmark gốc
Nghiên cứu đã hoàn tất đánh giá toàn bộ 645 đối tượng đủ điều kiện trong danh mục hiện có, thay vì chỉ trình bày một số trường hợp nhỏ. Khái niệm toàn phạm vi trong báo cáo gắn với 169 mô-đun và 21 dự án có môi trường nguồn mã phù hợp; nó không có nghĩa mọi mô-đun của benchmark Test4Py gốc hoặc mọi cấu hình hệ thống đều đã được chạy.

Để khẳng định cải tiến so với Test4Py, bước tiếp theo cần cố định đúng phiên bản benchmark và chạy cả hai quy trình trên cùng đối tượng, mô hình hoặc ngân sách tương đương, số lần sửa và môi trường. Chạy thêm nhiều đối tượng trong các dự án đã quan sát giúp làm rõ hiệu quả trong phạm vi đó; bổ sung dự án hoàn toàn mới mới trực tiếp mở rộng số cụm kiểm tra khả năng khái quát.

Đánh giá lỗi thực cũng là hướng bổ sung quan trọng. Có thể sử dụng cặp phiên bản lỗi và đã sửa trong BugsInPy [24], giữ bộ kiểm thử chuẩn ngoài lời nhắc và chỉ ghi nhận phát hiện khi kiểm thử chạy đúng trên bản đã sửa nhưng nhận biết được sai lệch trên bản có lỗi. Các mở rộng này phục vụ câu hỏi nghiên cứu đã xác định, không nhằm tìm tập con thuận lợi hoặc bảo đảm trước một giá trị p.

# CHƯƠNG 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
## 5.1. Kết luận theo câu hỏi nghiên cứu
Đề tài đã triển khai quy trình sinh và sửa kiểm thử Python dựa trên ngữ cảnh mã nguồn, thông tin thiết lập và phản hồi thực thi. Nội dung cải tiến nằm ở việc làm rõ giao diện sử dụng và tập trung ngữ cảnh liên quan trong ngân sách nhỏ. Kết quả được đánh giá qua đối chứng thành phần, phân tích quá trình phát triển và một ứng dụng có kiểm thử tái sử dụng.

@table conclusions | Bảng 5.1. Tổng hợp câu trả lời cho bốn câu hỏi nghiên cứu

Đối chứng toàn phạm vi hoàn tất 3.870 lượt trên 645 đối tượng thuộc 21 dự án. Tương phản chính giữa ngữ cảnh kết hợp và mã nguồn là {{PRIMARY_DIFF}} điểm phần trăm, với khoảng tin cậy 95% từ {{PRIMARY_LO}} đến {{PRIMARY_HI}} điểm. {{PRIMARY_INTERPRETATION}} Dữ liệu chưa cung cấp đối chứng toàn quy trình để khẳng định vượt Test4Py đầy đủ.

Giá trị ứng dụng cụ thể được ghi nhận từ giai đoạn 14B: bộ 14 ca giữ nguyên 12 ca cũ, tăng độ phủ genty_args từ 18/20 lên 20/20 dòng và phát hiện hai biến đổi hành vi mà bộ cũ bỏ sót. Kết quả này cho thấy có thể tái sử dụng kiểm thử sinh thật, đồng thời nhấn mạnh sự khác biệt giữa cải thiện một bộ kiểm thử cụ thể và chứng minh hiệu quả tổng quát của thuật toán.

## 5.2. Hướng phát triển
Sau khi hoàn tất khung đủ điều kiện hiện có, hướng ưu tiên là mở rộng tới đúng phiên bản benchmark gốc và bổ sung dự án độc lập để kiểm tra khả năng chuyển giao. Trong thiết kế thành phần, cần tách ngữ cảnh phụ trợ, thiết lập và sửa lỗi thành các nhánh đối chứng có ngân sách tương đương. Với đánh giá toàn quy trình, cần đối chứng trực tiếp với Test4Py thay vì so các số tổng hợp khác phạm vi.

Nghiên cứu tiếp theo cũng cần tăng chất lượng thông tin thiết lập, rà soát cơ sở xác định kết quả mong đợi và dùng lỗi thực hoặc tập đột biến được chọn trước. Các thay đổi này nhằm chuyển từ tín hiệu cải thiện trong thực nghiệm thăm dò sang bằng chứng có độ tin cậy và phạm vi khái quát rõ ràng hơn.
