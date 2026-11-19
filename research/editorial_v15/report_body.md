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
Đối tượng nghiên cứu là bộ kiểm thử do mô hình ngôn ngữ sinh cho các hàm và lớp thuộc thư viện Python công khai. Tập dự án thực tế bổ sung được xây dựng từ danh mục mô-đun tham khảo các bộ chuẩn đánh giá (benchmark), sử dụng bản phát hành đã cố định của phần mềm mã nguồn mở bên ngoài. Đánh giá trọng tâm bao phủ toàn bộ 645 đối tượng đủ điều kiện trên 169 mô-đun thuộc 21 dự án trong danh mục hiện có. Ba cấu hình ngữ cảnh và hai lượt lặp tạo 3.870 lượt đánh giá. Giai đoạn phát triển trên 21 đối tượng, hai đợt đối chứng nhỏ hơn và các khảo sát vận hành được giữ làm bằng chứng bổ trợ. Các đợt có thiết kế khác nhau được dùng để trả lời các khía cạnh tương ứng của cùng bài toán, không cộng thành một mẫu thống kê đồng nhất.

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

## 1.3. Khoảng trống nghiên cứu và hướng cải tiến được khảo sát
Thông tin bổ sung chỉ có ích khi liên quan tới hành vi cần kiểm tra và đủ ngắn để mô hình sử dụng được. Đề tài khảo sát ba cơ chế: bổ sung khai báo phụ trợ từ mã nguồn, cung cấp thiết lập đầu vào đã được thực thi thử và sử dụng kết quả chạy kiểm thử để định hướng sửa lỗi. Mục đích là giảm sai sót về giao diện và trạng thái, đồng thời giữ ngân sách suy luận nhỏ.

Thông tin thiết lập cho biết một cách gọi đã hoàn tất trong môi trường đánh giá; thông tin này không cung cấp giá trị đầu ra mong đợi cho kiểm thử. Phân biệt giữa thông tin về cách sử dụng và điều kiện khẳng định giúp hạn chế việc đưa sẵn đáp án kiểm thử vào ngữ cảnh.

Khoảng trống được khảo sát là liệu thông tin sử dụng thu được với chi phí thấp có đủ giúp mô hình tạo kiểm thử khả dụng, khi không xây dựng phân tích ngữ nghĩa liên thủ tục toàn dự án. Đây là bài toán đánh đổi giữa mức thông tin, chi phí thu thập ngữ cảnh và độ tin cậy đầu ra. Bổ sung nhiều mã hơn có thể làm rõ phụ thuộc nhưng cũng tăng nhiễu; một cách khởi tạo chạy được có thể giảm lỗi đầu vào nhưng lại hướng mô hình về một số trạng thái hẹp. Vì vậy, lợi ích của ngữ cảnh phải được kiểm tra bằng đối chứng thành phần, không được giả định từ độ dài lời nhắc.

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
## 3.1. Mô hình bài toán, mục tiêu và giả thuyết
Gọi f là đối tượng cần kiểm thử, M là mô-đun chứa f và E là môi trường thực thi đã cố định. Một chính sách ngữ cảnh lựa chọn thông tin từ M và các phép thử thiết lập để tạo C. Mô hình L nhận C cùng yêu cầu kiểm thử và sinh bộ T. Đầu ra nghiên cứu không chỉ là văn bản T mà còn là bằng chứng T được thu thập, thực thi và chạm tới phần thân f trong E. Mục tiêu thực nghiệm là tăng xác suất tạo bộ kiểm thử đáp ứng tiêu chí đã xác định, với ngân sách ngữ cảnh, đầu ra và sửa lỗi hữu hạn.

Mô hình bài toán phân biệt ba loại ràng buộc. Ràng buộc giao diện quyết định cách nhập và gọi đúng đối tượng. Ràng buộc trạng thái quyết định tiền điều kiện để hành vi có thể được thực thi. Ràng buộc ngữ nghĩa quyết định kết quả nào cần được khẳng định. Hai loại đầu chủ yếu liên quan tới tính khả thi của đầu vào; loại cuối liên quan tới test oracle. Phương pháp tác động trực tiếp vào hai loại đầu và cung cấp thêm bằng chứng mã nguồn cho loại cuối, nhưng không coi một lời gọi thử thành công là chứng minh kết quả mong đợi.

Ba nhánh dùng chung mô hình sinh và yêu cầu đầu ra. Nhánh A chỉ có mã đối tượng và các lệnh nhập. Nhánh B thêm thông tin thiết lập đã được thực thi thử khi có. Nhánh C giữ chính sách thiết lập của B và thêm khai báo phụ trợ có giới hạn. So sánh C với A trả lời câu hỏi hiệu quả chính sách kết hợp; B với A khảo sát thiết lập; C với B khảo sát giá trị tăng thêm của khai báo phụ trợ. Thiết kế chưa có nhánh chỉ khai báo phụ trợ nên không tách được đầy đủ tương tác giữa hai thành phần như một thiết kế nhân tố hai nhân hai.

@table hypotheses | Bảng 3.1. Giả thuyết cơ chế và bằng chứng dùng để đánh giá

Đích tối ưu được đo bằng tỷ lệ bộ khả dụng theo dự án dưới cùng ngân sách, không phải tối đa độ dài ngữ cảnh hoặc chỉ làm mọi kiểm thử vượt qua.

Bảng giả thuyết hệ thống hóa lập luận nghiên cứu trong bản trình bày; các giả thuyết cơ chế không phải kết luận đã được xác nhận. Kế hoạch tương phản thống kê được cố định trước đợt lớn, còn các phân tích phân nhóm bổ sung ở Chương 4 là hậu kiểm mô tả.

@figure architecture | Hình 3.1. Quy trình sinh và đánh giá kiểm thử dựa trên ngữ cảnh và phản hồi thực thi

Nguồn: thiết kế của nghiên cứu. Trong đối chứng chính, số lượt sửa bằng không để đo hiệu quả ngữ cảnh ở lần sinh đầu; vòng phản hồi thuộc phạm vi đánh giá phát triển riêng.

## 3.2. Chính sách lựa chọn ngữ cảnh và xác nhận thiết lập
### 3.2.1. Khai báo phụ trợ theo quan hệ tham chiếu cục bộ
Ngữ cảnh cơ sở giữ khai báo đối tượng và các lệnh nhập của mô-đun. Phần mở rộng xem mỗi khai báo cấp mô-đun là một đỉnh; quan hệ từ khai báo u tới v tồn tại khi trong u có tên được đọc khớp với tên khai báo v trong cùng mô-đun. Mở rộng tối đa hai mức thu được phần giải thích cục bộ cho các hàm phụ trợ, lớp hoặc hằng số mà đối tượng sử dụng. Đây là quan hệ tham chiếu cú pháp, không phải đồ thị gọi đã phân giải đầy đủ: tên cục bộ trùng tên, truy cập thuộc tính, gọi động và phụ thuộc qua mô-đun khác có thể không được mô hình hóa chính xác.

Quy tắc giữ ngữ cảnh là xác định: xét tên theo thứ tự ổn định, không xét lại cùng một tên đã thu thập và chỉ thêm khai báo nằm trong giới hạn. Mỗi khai báo phụ trợ tối đa 4.000 ký tự, tổng nội dung khai báo tối đa 8.000 ký tự, chưa tính dấu phân cách; khai báo quá giới hạn bị bỏ qua thay vì cắt tùy ý giữa cấu trúc. Giới hạn ký tự là ràng buộc trích xuất, không tương đương giới hạn token của mô hình. Số token thực tế được đo từ phản hồi dịch vụ.

Một khai báo gán đồng thời nhiều tên vẫn có thể được đưa vào nhiều lần; chính sách hiện tại loại lặp theo tên, chưa loại lặp theo khai báo.

Lựa chọn mở rộng cục bộ nhằm giảm chi phí phân tích và giới hạn lượng thông tin không trực tiếp phục vụ đối tượng. Với mô-đun có n nút AST, một lượt duyệt thu thập khai báo có chi phí tỷ lệ với n; việc đọc lại tối đa hai mức vẫn bị chặn bởi kích thước nguồn và ngân sách trích xuất. Lập luận này mô tả tính chất của chính sách, không phải phép đo thời gian hoặc bằng chứng tối ưu. Đánh đổi là bỏ sót phụ thuộc liên mô-đun và không suy ra đầy đủ tiền điều kiện động.

### 3.2.2. Thiết lập như bằng chứng khả thi, không phải đáp án kiểm thử
Thông tin thiết lập xuất phát từ chữ ký và một chính sách đối số tối thiểu cố định. Tham số có mặc định được bỏ qua; tham số bắt buộc được gán ứng viên theo nhóm tên hoặc chú thích kiểu, gồm giá trị logic, danh sách rỗng, hàm gọi lại đơn giản hoặc giá trị số mặc định. Tham số chỉ nhận theo vị trí chưa được chính sách hỗ trợ. Chi tiết ứng viên được cố định trước khi sinh kiểm thử, không tìm kiếm lại theo kết quả đánh giá.

Mỗi phép thử có giới hạn 10 giây và chạy trong tiến trình riêng. Chỉ chữ ký và đối số của lời gọi hoàn tất mới đi vào ngữ cảnh; giá trị trả về và nội dung in ra của chương trình không được dùng làm đáp án. Với lớp, phép thử xác nhận một cách gọi hàm tạo; với hàm, nó xác nhận một lời gọi đã hoàn tất. Cả hai đều không chứng minh tính đại diện của dữ liệu hay tiền điều kiện của mọi phương thức.

@algorithm context | Thuật toán 3.1. Xây dựng ngữ cảnh theo chính sách cố định

Nếu không thu được gợi ý thiết lập hoặc khai báo phụ trợ, đối tượng vẫn được giữ ở nhánh đã chỉ định. Vì vậy, đại lượng được ước lượng là hiệu quả chính sách áp dụng trên toàn tập đủ điều kiện, gồm cả trường hợp không cung cấp thêm thông tin. Chỉ phân tích các phép thử thiết lập thành công sẽ đổi bài toán sang một tập đối tượng dễ hơn và làm mất tính tương ứng với thiết kế ban đầu.

## 3.3. Sinh kiểm thử và phản hồi có kiểm soát
Một bộ kiểm thử phải thể hiện ba phần: chuẩn bị trạng thái, kích hoạt hành vi và khẳng định thuộc tính quan sát được. Lời nhắc yêu cầu ba hàm kiểm thử cấp mô-đun, tập trung vào trường hợp thông thường, điều kiện biên hoặc ngoại lệ có căn cứ. Ba hàm là quy cách đầu ra chung, không bảo đảm mỗi hàm thuộc một loại hành vi cố định và không được xem là ba mẫu thống kê độc lập.

Ở đợt chính, số lần sửa bằng không. Lựa chọn này loại bỏ sự khác biệt về số cơ hội sửa và lượng phản hồi, để tương phản giữa các nhánh tập trung vào ngữ cảnh đầu vào. Đổi lại, tỷ lệ đạt phản ánh chất lượng sinh ở lần đầu dưới quy cách ba hàm, không phải khả năng tối đa của một hệ sinh kiểm thử có sửa lặp hoặc tích lũy độ phủ.

Trong phạm vi quy trình có phản hồi, kết quả thu thập và dấu vết ngoại lệ hỗ trợ mô hình sửa kiểm thử, tối đa hai lượt. Phân biệt lỗi giao diện, lỗi thiết lập và lỗi khẳng định giúp định hướng sửa, nhưng chưa có bằng chứng mọi lần sửa bảo toàn ý nghĩa. Vì vậy, thành công vận hành sau sửa và bảo toàn oracle là hai tiêu chí riêng. Các kết quả phát triển được dùng để hình thành giả thuyết về vai trò phản hồi, không thay thế đối chứng ngữ cảnh trên tập lớn.

@algorithm feedback | Thuật toán 3.2. Sinh và đánh giá với ngân sách sửa hữu hạn

Các lời nhắc tiếng Anh đã dùng được giữ ở Phụ lục 1. Bộ kiểm thử sinh ra được chạy trên mã sản phẩm đã cố định. Không sửa mã sản phẩm hoặc loại ca thất bại để thay đổi kết quả chấp nhận của một lượt đã lên lịch.

## 3.4. Định nghĩa chỉ số và đơn vị phân tích
Một lượt tương ứng với bộ ba đối tượng, nhánh và giá trị seed. Gọi A của lượt bằng 1 khi tất cả điều kiện chấp nhận thỏa mãn, bằng 0 khi đầu ra đã quan sát không thỏa. Các điều kiện gồm mã trích xuất được, đúng ba hàm kiểm thử cấp mô-đun, vượt kiểm tra cấu trúc, tất cả hàm được thu thập và các ca đều vượt qua, độ phủ mô-đun dương, có dòng thực thi thuộc phần thân đối tượng, đồng thời chạy lại đạt và khớp độ phủ dòng. Đối với lớp, chứng kiến một phần thân phương thức chưa chứng minh bao phủ tất cả phương thức.

@table metrics | Bảng 3.2. Chỉ số, mẫu số và giới hạn diễn giải

Với một nhánh, tỷ lệ theo lượt bằng tổng A chia cho 1.290 lượt. Với dự án p có n đối tượng và hai lượt lặp, tỷ lệ riêng bằng tổng A của dự án chia cho 2n. Tỷ lệ cân bằng dự án là trung bình của 21 tỷ lệ riêng. Có thể viết ngắn gọn: PR(p,a) = số bộ đạt của dự án p ở nhánh a / số lượt dự kiến của dự án p. Tỷ lệ cân bằng bằng tổng PR(p,a) / 21.

Quy tắc thứ nhất trả lời thu được bao nhiêu bộ đạt trong tập đang chạy; quy tắc thứ hai cho mỗi dự án cùng trọng số khi tổng hợp. Hai đại lượng có thể khác hướng thay đổi khi quy mô dự án không bằng nhau.

Độ phủ câu lệnh mô-đun bằng 100 nhân số dòng có thể thực thi đã được chạy chia cho tổng số dòng có thể thực thi. Độ phủ nhánh dùng số nhánh đã thực thi chia cho tổng số nhánh cần đo; không có nhánh thì ghi không áp dụng. Chỉ số độ phủ có tính lượt không đạt dùng tích A với độ phủ mô-đun của lượt, lấy trung bình theo dự án rồi trung bình giữa 21 dự án. Đây là chỉ số tổng hợp có phạt, không phải độ phủ thuần trên các bộ chạy thành công. Dữ liệu độ phủ thiếu vẫn được giữ là thiếu trong hồ sơ gốc.

Bằng chứng chạm thân đối tượng chỉ đòi hỏi giao giữa dòng thực thi và dòng trong thân hàm hoặc phương thức khác rỗng; nó ngăn ghi nhận chỉ nhập mô-đun mà không kích hoạt đối tượng. Không dùng điều kiện này để thay thế độ phủ mục tiêu hoặc chất lượng khẳng định. Tương tự, tỷ lệ chạy lại được tính trên các bộ đã được nhận, không phải trên toàn bộ 3.870 đầu ra.

Khảo sát ghép gói sử dụng mọi bộ đã nhận của một dự án và nhánh ở cả hai lượt lặp. Độ phủ gói được đo trên hợp các tệp nguồn thuộc danh mục đủ điều kiện của dự án, bao gồm tệp chưa được thực thi; không cộng các tỷ lệ độ phủ từng bộ. Chỉ số gói hợp lệ ghi nhận độ phủ khi toàn gói vượt qua và thu thập đủ ca, còn gói không đạt đóng góp bằng không khi tổng hợp 21 dự án. Mẫu số này khác độ phủ một mô-đun ở cấp lượt nên hai mức không được so trực tiếp như cùng một phép đo.

Kiểm thử đột biến báo cáo đồng thời số phát hiện, không phát hiện và chưa thể kết luận trên mẫu đã lên lịch. Chỉ ghi nhận phát hiện hành vi khi bộ kiểm thử vượt qua trên bản gốc và thất bại do kiểm tra hành vi trên bản biến đổi; lỗi thu thập hoặc hết thời gian không mặc nhiên được tính là phát hiện.

## 3.5. Thiết kế đánh giá trên tập dự án thực tế bổ sung
Đánh giá chính được thiết kế như một thực nghiệm trên tập dự án thực tế bổ sung, nhằm kiểm tra các cấu hình ngữ cảnh của phương pháp trong cùng điều kiện. Tập này sử dụng toàn bộ 645 hàm hoặc lớp đáp ứng tiêu chí nguồn mã trong các danh mục đã lưu. Các đối tượng thuộc 169 mô-đun và 21 dự án; không chỉ giữ vài trường hợp đại diện. Danh sách, phiên bản môi trường, lời nhắc, số lượt lặp và kế hoạch phân tích được cố định trước khi gọi mô hình cho đợt này.

Ba nhánh được so sánh ghép cặp gồm chỉ mã nguồn, mã nguồn kèm thiết lập đã thử, và mã nguồn kèm cả thiết lập lẫn khai báo phụ trợ. Mỗi đối tượng có hai lượt lặp, với giá trị seed 71 và 72 được gửi qua API. Cả ba nhánh sử dụng GPT-OSS-20B, nhiệt độ 0,2, giới hạn 2.048 token đầu ra và không sửa lỗi, tạo tổng cộng 3.870 lượt, tương ứng 1.290 lượt mỗi nhánh. Việc ưu tiên ba cấu hình giúp đánh giá đóng góp thành phần trên cùng tập đối tượng; số lượt lặp không thay thế số dự án độc lập.

@table design | Bảng 3.3. Thiết kế đánh giá chính và các nguồn bằng chứng bổ trợ

Tập đối tượng gồm 357 hàm và 288 lớp. Độ dài khai báo trung vị là 22 dòng, với khoảng tứ phân vị từ 12 đến 42 dòng; tiêu chí chọn nguồn mã vì vậy cần được xét khi khái quát tới các lớp lớn hơn hoặc hệ thống tích hợp.

Thông tin thiết lập dùng được ở 337/645 đối tượng; phần khai báo phụ trợ có ở 388/645 đối tượng. Khi không có một loại thông tin bổ sung, đối tượng vẫn được giữ trong mẫu đánh giá và nhánh tương ứng dùng phần ngữ cảnh còn lại. Tương phản vì vậy đo hiệu quả của một chính sách bổ sung thông tin khi có thể thu được, không giả định mọi đối tượng đều có gợi ý hoàn hảo.

Điều kiện đủ tiêu chí được xác định từ nguồn mã trước suy luận: khai báo công khai ở cấp mô-đun, dài từ 5 đến 160 dòng và phần khai báo đối tượng không quá 6.000 ký tự. Danh mục mô-đun tham khảo các dự án liên quan tới Test4Py và CodaMOSA [1], [23]. Đối tượng được kiểm thử là mã nguồn của 21 dự án mã nguồn mở bên ngoài, chẳng hạn HTTPie, isort, Sanic và Tornado; kho triển khai của đề tài cung cấp phương pháp và bộ chạy, không phải phần mềm được dùng làm đối tượng đánh giá. Mã thực thi lấy từ các bản phát hành PyPI đã cố định phiên bản, có lưu thông tin môi trường và mã băm nguồn để kiểm tra lại. Đây là tập đánh giá bổ sung được xây dựng từ phần mềm thực tế, không phải bản sao nguyên trạng của benchmark hoặc thí nghiệm trong công trình gốc.

Nghiên cứu kế thừa bài toán và một số định hướng phương pháp từ Test4Py, nhưng sử dụng cấu hình mô hình và thiết kế ngữ cảnh riêng. Giai đoạn triển khai tại chỗ dùng mô hình 14B lượng tử hóa NF4; đánh giá diện rộng sử dụng GPT-OSS-20B qua Groq. Sự khác biệt về mô hình, phiên bản mã nguồn và quy trình khiến các tỷ lệ công bố của paper gốc không phải đối chứng trực tiếp. Đối chứng chính của nghiên cứu là ba nhánh dùng cùng GPT-OSS-20B, cùng đối tượng, ngân sách sinh và tiêu chí đánh giá, qua đó đo đóng góp của từng chính sách cung cấp ngữ cảnh.

Các nhánh chạy luân phiên trong từng cặp đối tượng và lượt lặp. Cơ chế thu thập được tăng từ HTTP tuần tự lên tối đa tám yêu cầu đồng thời theo yêu cầu điều phối, trong trần 1.000 yêu cầu và 250.000 token mỗi phút. Các tham số sinh, đối tượng và tiêu chí đánh giá giữ nguyên; giai đoạn điều phối được ghi riêng khi diễn giải thời gian và tài nguyên. Kiểm thử được thực thi trong tiến trình riêng, dùng môi trường phụ thuộc của dự án và cùng giới hạn thời gian 20 giây mỗi lần chạy. Đầu ra phải có đúng ba hàm kiểm thử cấp mô-đun; cả ba hàm phải được pytest thu thập và chạy thành công. Các trường hợp tham số hóa được tính là các ca trong ba hàm này, không phải đối tượng thống kê mới.

Trong 645 đối tượng, 61 đã được dùng ở hai đợt đối chứng chuẩn hóa trước, còn 584 chưa nằm trong hai tập đối chứng đó. Tuy nhiên, cả 21 dự án đều đã được quan sát trong quá trình triển khai. Đợt này đánh giá độ bao quát trong khung đã xác định, không được gọi là xác nhận trên 21 dự án hoàn toàn mới. Các số liệu cũ không được cộng vào 3.870 lượt của đối chứng chính.

### 3.5.1. Môi trường, thành phần và tham số kiểm soát
@table environment | Bảng 3.4. Môi trường và thành phần thực nghiệm đã ghi nhận

Nguồn: cấu hình đã khóa, kiểm tra môi trường của 21 dự án và hồ sơ thực thi. Python 3.10.22, pytest 9.2.0, coverage.py 7.16.2 và pytest-json-report 1.5.0 được đối chiếu theo từng môi trường dự án. Có 2.020 tệp nguồn sản phẩm được kiểm tra khớp bản lưu; đây là kiểm tra tính nhất quán giữa quá trình chạy, không được mô tả thành kiểm tra trước suy luận nếu thời điểm không phù hợp. Phiên bản cụ thể của 21 gói được trình bày ở phụ lục.

Máy khách điều phối gửi yêu cầu tới Groq và thực thi kiểm thử trong các môi trường Python riêng của dự án. Phần cứng phục vụ suy luận của API không do nghiên cứu kiểm soát. Hồ sơ đợt lớn chưa đủ thông tin để công bố cấu hình CPU, RAM và hệ điều hành của máy khách tại thời điểm chạy như một cấu hình phần cứng đã khóa; vì vậy, nghiên cứu không dùng các phép đo này để khẳng định tốc độ suy luận hoặc so sánh phần cứng. Sự thiếu hụt thông tin làm hạn chế tái lập thời gian, dù mã nguồn, phụ thuộc, đầu ra và quy tắc đánh giá vẫn có thể đối chiếu.

Các tiến trình kiểm thử dùng thư mục làm việc và biến môi trường tối thiểu riêng; đây là cách ly tiến trình, không phải bảo đảm an toàn của hộp cát hệ điều hành. Giới hạn 20 giây là một phần định nghĩa đầu ra sử dụng được trong môi trường này. Khi tăng từ hai lên sáu tiến trình đánh giá đồng thời, tải máy có thể ảnh hưởng các ca gần ngưỡng thời gian; việc giữ nguyên thời hạn không đủ để chứng minh hoàn toàn loại bỏ tác động điều phối.

### 3.5.2. Kịch bản kiểm tra và quy tắc diễn giải
@table scenarios | Bảng 3.5. Ma trận kịch bản, biến thay đổi và kết quả cần quan sát

Các kịch bản hình thành một chuỗi bằng chứng: sinh được bộ khả dụng ở cấp đối tượng, kiểm tra khả năng chạy lại, ghép thành gói dự án và xem xét khả năng phát hiện thay đổi hành vi. Không yêu cầu kết quả mọi cấp cùng chiều. Khả năng chạy riêng tốt hơn nhưng ghép gói kém hơn gợi ý kiểm tra tính độc lập trạng thái và điều kiện tích hợp, thay vì chọn một chỉ số thuận lợi làm đại diện toàn bộ chất lượng.

## 3.6. Phân tích thống kê và khả năng tái lập
Tương phản chính đã khóa là nhánh ngữ cảnh kết hợp thiết lập trừ nhánh chỉ mã nguồn. Hai tương phản phụ là thiết lập trừ mã nguồn và ngữ cảnh kết hợp trừ thiết lập. Tương phản phụ thứ hai đo phần giá trị bổ sung của khai báo phụ trợ khi giữ cùng chính sách thiết lập.

Với dự án p và tương phản C trừ A, đặt d(p) bằng tổng chênh lệch chấp nhận của các cặp đối tượng và seed chia cho số cặp của dự án. Hiệu ứng chính bằng tổng d(p) chia cho 21. Hiệu ứng chính theo điểm phần trăm bằng 100 nhân trung bình 21 giá trị d(p). Giả thuyết không của kiểm định đổi dấu là không có hiệu ứng theo cơ chế hoán đổi dấu đã nêu, còn câu hỏi thực tiễn là độ lớn chênh lệch và mức bất định có đủ hữu ích dưới cùng ngân sách hay không. Đơn vị hiệu ứng được báo theo điểm phần trăm, phân biệt với phần trăm tăng tương đối. Ghép cặp kiểm soát khác biệt đối tượng và tham số sinh, nhưng cùng seed qua API không bảo đảm hai nhánh có cùng chuỗi ngẫu nhiên nội bộ. Báo cáo đồng thời trình bày tỷ lệ theo lượt để mô tả số bộ kiểm thử sử dụng được và tỷ lệ cân bằng dự án để phân tích khả năng chuyển giao. Độ phủ có tính lượt không đạt cũng được báo theo cùng cách cân bằng khi dùng cho đánh giá chính.

Khoảng tin cậy 95% sử dụng 20.000 lần lấy mẫu lại theo cụm dự án, với giá trị khởi tạo 20261119. Kiểm định đổi dấu hai phía được tính ở cấp 21 dự án. Phép kiểm định cần giả định độc lập và khả năng hoán đổi dấu của chênh lệch dưới giả thuyết không; việc ghép cặp tự nó không bảo đảm các giả định này. Hai giá trị p của các tương phản phụ được hiệu chỉnh bằng phương pháp Holm; tương phản chính được xác định riêng trước chạy. Các khoảng tin cậy là khoảng biên cho từng tương phản, không phải khoảng đồng thời.

Với 21 dự án, kiểm định xét toàn bộ 2.097.152 cách đổi dấu của các chênh lệch dự án và đếm tỷ lệ có độ lớn trung bình ít nhất bằng giá trị quan sát. Lấy mẫu lại giữ nguyên cấu trúc ghép cặp bên trong dự án, tránh tách các lượt của cùng thư viện thành các mẫu độc lập. Khoảng percentile và kiểm định đổi dấu là hai thủ tục khác nhau, vì vậy không bắt buộc cho cùng quyết định ở sát ngưỡng; khoảng biên dương của một tương phản phụ không thay thế kiểm soát nhiều phép thử. Giá trị p lớn cũng không chứng minh hai chính sách tương đương: để kết luận tương đương cần đặt trước biên sai khác có ý nghĩa thực tiễn và một thiết kế phù hợp.

Phân tích kết luận chỉ được thực hiện khi có đủ toàn bộ tích các đối tượng, ba nhánh và hai lượt lặp. Không dừng nghiên cứu khi thấy kết quả thuận lợi. Mọi đầu ra mô hình không đạt tiêu chí vẫn nằm trong mẫu số. Sự cố truyền thông, bằng chứng hỏng hoặc nguồn mã bị thay đổi làm tạm dừng để đối chiếu, không bị chuyển thành một kết quả chất lượng mô hình đã quan sát.

Mỗi lượt lưu lời nhắc, đầu ra mô hình, mã kiểm thử và kết quả thực thi. Các bộ được nhận còn được chạy lại độc lập. Khả năng tái lập trong báo cáo được hiểu là chạy lại thực nghiệm của chính đề tài từ hồ sơ đã lưu, cần phân biệt với tái lập công trình Test4Py. Chạy lại đầu ra đã lưu và tính lại thống kê là hai mức có thể kiểm tra trực tiếp. Sinh mới qua API là một mức khác, chịu ảnh hưởng của dịch vụ và phiên bản mô hình cung cấp.

# CHƯƠNG 4. THỰC NGHIỆM VÀ ĐÁNH GIÁ
## 4.1. Tổ chức đánh giá theo câu hỏi nghiên cứu
Phần thực nghiệm lấy đợt bao phủ toàn bộ danh mục đủ điều kiện làm kết quả trung tâm. Đợt này hoàn tất 3870 trên 3.870 lượt dự kiến, bao gồm cả các lượt không sinh được mã hợp lệ hoặc không vượt qua kiểm thử. Các bằng chứng phát triển, vòng sửa lỗi và ứng dụng 14B được dùng để giải thích cơ chế và giá trị sử dụng, thay vì trở thành những thực nghiệm nhỏ tách rời.

RQ1 được trả lời bằng tương phản chính giữa ngữ cảnh kết hợp và mã nguồn. RQ2 được phân tích qua hai tương phản thành phần trên cùng tập, cùng bằng chứng phản hồi ở giai đoạn phát triển. RQ3 sử dụng chạy lại và kiểm tra thay đổi hành vi; RQ4 đánh giá tài nguyên và ngân sách. Các kết quả cũ giữ mẫu số riêng và được đặt trong tiến trình phát triển phương pháp.

## 4.2. Kết quả trên toàn bộ 645 đối tượng đủ điều kiện
### 4.2.1. Khả năng tạo bộ kiểm thử sử dụng được
Bảng 4.1 trình bày ba cấu hình trên cùng 645 đối tượng thuộc 21 dự án. Số lượt đạt theo mẫu số 1.290 mô tả sản phẩm kiểm thử thu được. Tỷ lệ và độ phủ cân bằng dự án tránh để các thư viện có nhiều đối tượng chi phối kết luận.

@table primary | Bảng 4.1. Kết quả ba cấu hình trên toàn bộ danh mục đủ điều kiện

Nguồn: kết quả đầy đủ của đợt đánh giá 3.870 lượt. Độ phủ được đo trên mô-đun, tính cả các lượt không đạt theo quy ước của mục 3.4.

Nhánh chỉ mã nguồn đạt 378/1.290 lượt (29,30%). Nhánh thêm thiết lập đạt 383/1.290 lượt (29,69%), còn nhánh ngữ cảnh kết hợp đạt 423/1.290 lượt (32,79%). Tỷ lệ cân bằng dự án tương ứng là 35,18%, 32,11% và 37,05%. Chênh lệch cân bằng dự án có thể khác chênh lệch tỷ lệ theo lượt do quy mô đối tượng giữa các dự án không bằng nhau.

### 4.2.2. Hiệu ứng phương pháp và đóng góp thành phần
@table contrasts | Bảng 4.2. Chênh lệch ghép cặp và mức bất định theo dự án

Nguồn: phân tích theo kế hoạch đã khóa. Chênh lệch và khoảng tin cậy dùng đơn vị điểm phần trăm. Hiệu chỉnh Holm áp dụng cho hai tương phản phụ; độ phủ là chỉ số mô tả.

Tương phản chính giữa ngữ cảnh kết hợp và mã nguồn là 1,86 điểm phần trăm, với khoảng tin cậy 95% từ -1,86 đến 5,59 điểm và p hai phía bằng 0,34644. Kết quả chưa cung cấp đủ bằng chứng thống kê về ưu thế của nhánh ngữ cảnh kết hợp trong thiết kế đã xét; mức chênh lệch dương là tín hiệu quan sát, chưa phải cải thiện tổng quát đã được xác nhận.

Tương phản thiết lập so với mã nguồn là -3,07 điểm phần trăm, với p đã hiệu chỉnh 0,28586. Khi giữ cùng thông tin thiết lập và bổ sung khai báo phụ trợ, chênh lệch là 4,94 điểm phần trăm, với p đã hiệu chỉnh 0,11050. Hai kết quả này giúp phân biệt phần giá trị của thiết lập với phần giá trị của khai báo phụ trợ, thay vì quy toàn bộ kết quả cho AST. Tương phản bổ sung khai báo có khoảng bootstrap dương nhưng chưa đạt ngưỡng 0,05 theo kiểm định đổi dấu và hiệu chỉnh Holm; không dùng riêng khoảng này để khẳng định ưu thế.

@figure effects | Hình 4.1. Hiệu ứng của phương pháp và hai tương phản thành phần theo dự án

Nguồn: phân tích cụm của đợt đánh giá đầy đủ. Mốc không trên trục hoành biểu thị hai nhánh có cùng tỷ lệ đạt. Các khoảng là khoảng tin cậy biên 95%.

Phân bố kết quả của toàn bộ 21 dự án được trình bày tại Phụ lục 2. Kết quả có thể khác nhau theo kiểu giao diện và mức thông tin bổ sung thu được; số đối tượng lớn không làm các dự án trở thành mẫu ngẫu nhiên của mọi phần mềm Python. Đợt toàn phạm vi làm rõ mức độ bao quát trong khung đã cố định, còn khả năng khái quát ra các dự án mới vẫn cần đánh giá riêng.

RQ1 được trả lời theo phạm vi tương phản chính và khoảng bất định đã báo. RQ2 về đóng góp thiết lập và khai báo phụ trợ được đánh giá bằng hai tương phản phụ cùng dữ liệu, thay vì chọn một tập con có kết quả tốt hơn.

## 4.3. Phân tích cơ chế và đánh đổi thiết kế
### 4.3.1. Đóng góp của thiết lập và khai báo phụ trợ
Thiết lập chỉ làm tăng số bộ đạt gộp từ 378 lên 383, trong khi tỷ lệ cân bằng dự án giảm 3,07 điểm phần trăm. Hai chỉ số trả lời câu hỏi khác nhau: số bộ thu được thiên về dự án có nhiều đối tượng, còn ước lượng cân bằng coi mỗi dự án là một đơn vị cùng trọng số. Sự khác biệt cho thấy không thể lấy tăng năm bộ làm bằng chứng thiết lập có lợi trên một dự án điển hình. Một lời gọi thiết lập tối thiểu có thể khả thi nhưng ít đại diện cho hành vi cần kiểm tra; đây là giả thuyết giải thích cần đối chứng thêm, chưa phải nguyên nhân được xác nhận.

Khi bổ sung khai báo phụ trợ trên cùng chính sách thiết lập, số bộ đạt tăng từ 383 lên 423. Thông tin cục bộ có thể giúp diễn giải giá trị hằng và quan hệ sử dụng, nhưng tác động quan sát còn bao gồm cách mô hình phản ứng với độ dài và cấu trúc ngữ cảnh. Chưa có đối chứng ngữ cảnh nhiễu cùng độ dài hoặc nhánh chỉ khai báo, nên không quy toàn bộ chênh lệch cho khả năng phân giải phụ thuộc của AST.

### 4.3.2. Kết quả ghép cặp và sự không đồng nhất
Trong 1.290 cặp cùng đối tượng và seed, có 264 cặp cả hai nhánh đạt, 159 chỉ nhánh kết hợp đạt, 114 chỉ nhánh mã nguồn đạt và 753 cả hai không đạt. Mức tăng ròng 45 bộ vì vậy đi cùng 273 cặp đổi trạng thái theo cả hai chiều; phương pháp không đơn thuần giữ mọi kết quả tốt của nhánh cơ sở rồi bổ sung thêm. Ở cấp dự án, nhánh kết hợp tăng tỷ lệ trên 9 dự án, không đổi trên 5 và giảm trên 7. Phân bố đầy đủ giải thích vì sao chênh lệch gộp dương chưa xác lập cải thiện nhất quán giữa các dự án.

@table paired | Bảng 4.3. Chuyển trạng thái chấp nhận trong các cặp cùng đối tượng và seed

Nguồn: phân tích mô tả hậu kiểm trên toàn bộ 1.290 cặp, không loại dự án hoặc seed theo kết quả. Bảng không tạo thêm phép kiểm định xác nhận ngoài kế hoạch đã khóa.

Phân tích hậu kiểm giữ đầy đủ hai nhóm hàm và lớp: nhánh kết hợp đạt 290/714 lượt trên hàm so với 260/714 của mã nguồn, và 133/576 trên lớp so với 118/576. Chênh lệch cân bằng dự án tương ứng là 3,21 và 0,54 điểm phần trăm. Hai nhóm có cơ cấu dự án khác nhau và loại đối tượng không được phân bổ ngẫu nhiên, nên không diễn giải thành tác động nhân quả riêng trên hàm hoặc lớp. Toàn bộ phân nhóm theo loại đối tượng, khả năng thiết lập và khai báo phụ trợ được giữ ở phụ lục, không chỉ trình bày nhóm thuận lợi.

Theo hai seed 71 và 72, chênh lệch cân bằng dự án của tương phản chính lần lượt là 1,90 và 1,83 điểm phần trăm. Chênh lệch thiết lập so với mã nguồn ở codetiming là một bộ trên hai lượt, tương ứng giảm 50 điểm phần trăm trong dự án chỉ có một đối tượng. Với trọng số dự án bằng nhau, dự án này đóng góp khoảng -2,38 điểm phần trăm vào tương phản thiết lập toàn tập. Điều đó giải thích độ nhạy của ước lượng ở dự án nhỏ; dự án vẫn được giữ nguyên trong phân tích đã khóa.

Cùng chiều ở hai seed là bằng chứng mô tả trong cấu hình đã đo; hai lượt chưa đủ khẳng định vững trên nhiều tham số sinh. Trong nhóm không có gợi ý thiết lập, khác biệt giữa nhánh B và A vẫn có thể do biến thiên sinh hoặc thực thi dù nội dung lời nhắc giống nhau; không quy chênh lệch đó cho thành phần chưa được cung cấp.

@figure project_effects | Hình 4.2. Phân bố chênh lệch chính trên đầy đủ 21 dự án

Nguồn: tổng hợp ghép cặp toàn bộ đối tượng và hai seed trong từng dự án. Hình thể hiện chênh lệch mô tả, không phải khoảng tin cậy riêng dự án.

@table failure_stages | Bảng 4.4. Phân bố kết quả và vị trí thất bại trên toàn bộ lượt đã lên lịch

Phân loại thất bại là phân tích hậu kiểm từ báo cáo pytest. Khi một lượt có nhiều lỗi, thứ tự ưu tiên là thu thập, thiết lập hoặc dọn dẹp, rồi thực thi hàm kiểm thử; nhờ đó các hàng loại trừ nhau và cộng đúng 1.290 cho mỗi nhánh. Đây là vị trí quan sát lỗi, chưa phải nguyên nhân ngữ nghĩa. Chẳng hạn, một lỗi trong hàm kiểm thử có thể do dùng API sai hoặc khẳng định sai, không tự chứng minh sản phẩm có lỗi.

Nhóm kết hợp giảm số lượt thất bại trong hàm kiểm thử từ 720 xuống 669 và lỗi thu thập từ 84 xuống 65, nhưng tăng nhóm không chạm thân đối tượng từ 29 lên 43 và lỗi thiết lập hoặc dọn dẹp từ 8 lên 23. Cấu trúc này gợi ý ưu tiên kiểm tra ràng buộc hành vi và tính độc lập trạng thái, thay vì chỉ tăng độ dài ngữ cảnh. Kết quả là giả thuyết thiết kế tiếp theo, chưa xác nhận một cơ chế nhân quả.

### 4.3.3. Phản hồi sửa lỗi và phạm vi bằng chứng
Ở giai đoạn phát triển, cấu hình trước tinh chỉnh đạt 67/105 ngay lần sinh đầu và thêm 29 lượt sau sửa, gồm 24 ở vòng thứ nhất và 5 ở vòng thứ hai. Kết quả cho thấy phản hồi có thể tận dụng một phần đầu ra chưa đạt, nhưng chưa tách được tác động nhân quả của phản hồi khỏi các khác biệt cấu hình và lựa chọn đối tượng. Giai đoạn này có hướng dẫn theo thư viện và tinh chỉnh trên đối tượng đã quan sát; không được xem như xác nhận hiệu quả sửa lỗi trên tập 645 đối tượng.

Các khảo sát lựa chọn cấu hình và đối chứng nhỏ trước đợt lớn được gom vào Phụ lục 4. Việc rút gọn phần thân nhằm giữ mạch lập luận, không thay đổi kết quả, mẫu số hay loại các khảo sát bất lợi. Kết luận chính vẫn dựa trên toàn bộ đợt lớn, gồm cả đầu ra thất bại.

## 4.4. Chất lượng kiểm thử và nghiên cứu ứng dụng 14B
### 4.4.1. Chạy lại và kiểm tra hành vi đã thực thi
Trong đợt toàn phạm vi, có 1184 bộ được nhận theo tiêu chí thực thi và chạy lại của quy trình. Kiểm tra độc lập tiếp theo chạy lại 1184 bộ: 1184 bộ vượt qua và 1184 bộ khớp độ phủ đã lưu. Các bộ được nhận đều tái chạy trong điều kiện đã kiểm tra; kết quả này không bảo đảm tính đúng đắn của mọi điều kiện khẳng định. Hai đợt đối chứng trước có 64 và 66 bộ được nhận đều chạy lại thành công; khảo sát phụ trợ cũ có thêm 23 bộ với cùng kết quả kiểm tra. Những số liệu này hỗ trợ khả năng tái chạy trong môi trường đã khóa; chúng không phải tỷ lệ ổn định của mọi đầu ra đã sinh.

Khả năng ghép các bộ được nhận thành gói chạy chung được khảo sát bổ sung trên toàn bộ 21 dự án và ba nhánh. Tất cả mã kiểm thử được giữ nguyên; mỗi dự án và nhánh tạo một gói, gồm cả hai lượt lặp. Số gói được công nhận hợp lệ theo thứ tự mã nguồn, thiết lập và kết hợp là 20/21, 18/21 và 17/21. Nhánh mã nguồn và kết hợp đều không có bộ được nhận ở dataclasses-json nên tạo một gói rỗng, không tính là lỗi kiểm thử đã thực thi. Các gói không rỗng nhưng thất bại gồm ba dự án ở nhánh thiết lập và ba dự án ở nhánh kết hợp; danh sách cùng báo cáo lỗi được giữ trong hồ sơ. Chênh lệch số bộ đã nhận cũng làm quy mô gói khác nhau, nên chưa thể quy mọi khác biệt tích hợp cho riêng loại ngữ cảnh. Độ phủ trung bình của gói hợp lệ trên toàn bộ 21 dự án tương ứng là 50,13%, 44,36% và 44,98%; gói không đạt đóng góp bằng không vào chỉ số tổng hợp. Độ phủ chưa đo được vẫn giữ là không có dữ liệu ở hồ sơ gốc. Đây là đánh giá khả năng tích hợp, được bổ sung khi đang thu thập dữ liệu, không thay thế kết quả chính hoặc kiểm định đã khóa.

Kết quả tích hợp không cùng chiều kết quả sinh riêng: nhánh kết hợp có 423 bộ được nhận nhưng chỉ 17/21 gói vượt qua, so với 378 bộ và 20/21 gói của nhánh mã nguồn. Độ phủ gói hợp lệ cũng thấp hơn ở nhánh kết hợp. Hai mức sử dụng mẫu số và phạm vi nguồn khác nhau nên không có mâu thuẫn số học; chúng cho thấy tính khả dụng từng bộ chưa bảo đảm khả năng cùng tồn tại trong một tiến trình. Khác biệt trạng thái dùng chung, thứ tự chạy hoặc tài nguyên là các hướng cần điều tra, chưa được quy kết là nguyên nhân nếu chưa có đối chứng riêng. Khảo sát gói được bổ sung khi đang thu thập dữ liệu nên chỉ mang vai trò thăm dò.

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

So với nhánh mã nguồn, nhánh kết hợp tăng token đầu vào khoảng 50,04% và tổng chi phí sử dụng ước tính khoảng 11,25%, trong khi số bộ đạt tăng 11,90%. Chi phí ước tính trên một bộ đạt chỉ giảm khoảng 0,58%; đây là đánh đổi vận hành rất nhỏ, không phải bằng chứng tối ưu kinh tế vững. Chỉ số này chưa gồm chi phí tiền xử lý, thử thiết lập, CPU chạy kiểm thử hoặc công sức phân tích. Vì vậy, kết luận khả thi trong ngân sách API được tách khỏi kết luận tối ưu tổng chi phí.

Khảo sát lựa chọn cấu hình trước đó trên 27 đối tượng đã quan sát dùng hai giới hạn 1.536 và 2.048 token, tổng 108 lượt. Không câu trả lời nào chạm giới hạn. Mức 1.536 token đạt 22/54 lượt và sử dụng 26.821 token đầu ra; mức 2.048 đạt 24/54 và dùng 25.439 token. Trong khảo sát này, hạ giới hạn không làm giảm số token thực tế. Nghiên cứu giữ mức 2.048 như khoảng dự phòng vận hành, không xem đây là bằng chứng đã tìm được mức tối ưu.

Sau đợt toàn phạm vi, sổ theo dõi API ghi 4558 phản hồi có thông tin sử dụng, với chi phí ước tính theo đơn giá cấu hình là 0,978099 USD. Tổng phân bổ bảo thủ là 1,425056 USD, gồm các khoản đặt trước và đối soát mốc ban đầu, nằm trong trần 3 USD. Riêng đợt toàn phạm vi có chi phí sử dụng ước tính 0,819876 USD. Hai số liệu phục vụ hai mục đích và không được cộng thành chi phí thực trả. Số phản hồi trong sổ theo dõi không phải cỡ mẫu thống kê của một đối chứng. Lịch gọi được điều tiết theo hạn mức dịch vụ; mọi sự cố và khoản đặt trước chưa quyết toán được giữ trong sổ theo dõi.

RQ4 cho thấy đánh giá thành phần qua API khả thi trong ngân sách đã theo dõi, còn triển khai 14B tại chỗ chịu ảnh hưởng lớn của khởi tạo và thời lượng thực thi. Thời gian chạy lại bộ kiểm thử trên CPU không được dùng để so tốc độ sinh của hai mô hình. Kết quả 14B được đánh giá thêm theo giá trị kiểm thử tái sử dụng thay vì chỉ theo tốc độ hạ tầng.

## 4.6. Tổng hợp bằng chứng và giới hạn suy luận
Đợt toàn phạm vi mở rộng bằng chứng từ vài đối tượng được chọn sang toàn bộ 645 đối tượng đủ điều kiện trong danh mục. Ba nhánh và hai lượt lặp được áp dụng theo cùng một thiết kế trên 21 dự án, giúp đánh giá phương pháp và thành phần trong một mạch thống nhất. Đóng góp của đợt lớn nằm ở việc tách được sản lượng theo lượt khỏi hiệu quả cân bằng dự án, chỉ ra chuyển trạng thái hai chiều và phân biệt kiểm thử chạy riêng với khả năng tích hợp. Những quan sát này định hướng lựa chọn chính sách ngữ cảnh tiếp theo; mức bất định của hiệu ứng chính được báo tại mục 4.2.2. Phạm vi kết luận vẫn là chính sách cung cấp ngữ cảnh trong môi trường và tiêu chí đã xác định, không phải ưu thế so với toàn bộ Test4Py.

Về tính hợp lệ của phép đo, chạy thành công và độ phủ không thay thế cơ sở xác định kết quả mong đợi. Chạy lại xác nhận sự nhất quán trong môi trường được kiểm tra; khảo sát đột biến nhỏ chỉ kiểm tra một phần độ nhạy hành vi. Các khảo sát đột biến lịch sử sử dụng bộ kiểm thử tuyển chọn nên được phân biệt với kết quả sinh kiểm thử của đợt toàn phạm vi.

Về tính hợp lệ nội tại, quy tắc ngữ cảnh và phân tích của đợt mới được khóa trước suy luận. Tuy nhiên, các dự án đã được quan sát và 61 đối tượng từng tham gia đối chứng trước. Giai đoạn phát triển cũ còn có hướng dẫn theo thư viện, ví dụ điều kiện khẳng định và tinh chỉnh trên đối tượng đã quan sát. Nghiên cứu giữ các bằng chứng phát triển này riêng, không coi là xác nhận khả năng tự xây dựng kết quả mong đợi trên dự án chưa biết.

Về kết luận thống kê, số lượt tăng lên 3.870 không tạo ra 3.870 dự án độc lập. Phân tích vẫn dựa trên 21 cụm dự án với các giả định đã nêu. Các thư viện công khai cũng có thể đã xuất hiện trong dữ liệu tiền huấn luyện của mô hình. Phiên bản package và phạm vi đủ tiêu chí khác benchmark gốc. Chưa có đối chứng toàn quy trình với Test4Py trên cùng điều kiện; độ phủ cao hoặc một tương phản có ý nghĩa thống kê không tự cung cấp đối chứng đó.

## 4.7. Phương án cải tiến tiếp theo từ kết quả thực nghiệm
Nghiên cứu đã hoàn tất đánh giá toàn bộ 645 đối tượng đủ điều kiện trong danh mục hiện có, thay vì chỉ trình bày một số trường hợp nhỏ. Khái niệm toàn phạm vi trong báo cáo gắn với 169 mô-đun và 21 dự án có môi trường nguồn mã phù hợp; nó không có nghĩa mọi mô-đun của benchmark Test4Py gốc hoặc mọi cấu hình hệ thống đều đã được chạy.

Mục tiêu của tập bổ sung là đánh giá tính khả thi và đóng góp thành phần trên mã nguồn thực tế, không yêu cầu tái lập toàn bộ thí nghiệm của Test4Py. So sánh giữa các nhánh trong cùng thiết kế cung cấp bằng chứng cho mục tiêu này; việc dùng mô hình khác không làm mất giá trị của đối chứng nội bộ. Tuy nhiên, kết quả chưa đủ để quy chênh lệch so với số liệu của công trình gốc cho riêng phương pháp. Nếu đặt câu hỏi so sánh trực tiếp với Test4Py, cần một thí nghiệm riêng kiểm soát tập đối tượng, mô hình, ngân sách, số lần sửa và môi trường. Hướng mở rộng trước mắt là bổ sung dự án chưa được quan sát và các bài toán kiểm tra hành vi thực tế.

@table decisions | Bảng 4.7. Kết quả quan sát, phương án đề xuất và phép kiểm tra tiếp theo

Các phương án ở Bảng 4.7 là hướng nghiên cứu tiếp theo, chưa được tính vào kết quả cải tiến đã đo. Một chiến lược chọn ngữ cảnh thích ứng chỉ hợp lệ khi quy tắc được phát triển trên tập riêng và khóa trước khi đánh giá dự án mới; chọn nhánh tốt nhất sau khi xem nhãn từng đối tượng sẽ dùng thông tin không có ở thời điểm triển khai.

Đánh giá lỗi thực cũng là hướng bổ sung quan trọng. Có thể sử dụng cặp phiên bản lỗi và đã sửa trong BugsInPy [24], giữ bộ kiểm thử chuẩn ngoài lời nhắc và chỉ ghi nhận phát hiện khi kiểm thử chạy đúng trên bản đã sửa nhưng nhận biết được sai lệch trên bản có lỗi. Các mở rộng này phục vụ câu hỏi nghiên cứu đã xác định, không nhằm tìm tập con thuận lợi hoặc bảo đảm trước một giá trị p.

# CHƯƠNG 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
## 5.1. Kết luận theo câu hỏi nghiên cứu
Đề tài đã triển khai quy trình sinh và sửa kiểm thử Python dựa trên ngữ cảnh mã nguồn, thông tin thiết lập và phản hồi thực thi. Nội dung cải tiến nằm ở việc làm rõ giao diện sử dụng và tập trung ngữ cảnh liên quan trong ngân sách nhỏ. Kết quả được đánh giá qua đối chứng thành phần, phân tích quá trình phát triển và một ứng dụng có kiểm thử tái sử dụng.

@table conclusions | Bảng 5.1. Tổng hợp câu trả lời cho bốn câu hỏi nghiên cứu

Đối chứng toàn phạm vi hoàn tất 3.870 lượt trên 645 đối tượng thuộc 21 dự án. Tương phản chính giữa ngữ cảnh kết hợp và mã nguồn là 1,86 điểm phần trăm, với khoảng tin cậy 95% từ -1,86 đến 5,59 điểm. Bằng chứng hiện có hỗ trợ tính khả thi và một số lợi ích quan sát được trong phạm vi khảo sát, chưa xác nhận ưu thế tổng quát. Dữ liệu chưa cung cấp đối chứng toàn quy trình để khẳng định vượt Test4Py đầy đủ.

Giá trị ứng dụng cụ thể được ghi nhận từ giai đoạn 14B: bộ 14 ca giữ nguyên 12 ca cũ, tăng độ phủ genty_args từ 18/20 lên 20/20 dòng và phát hiện hai biến đổi hành vi mà bộ cũ bỏ sót. Kết quả này cho thấy có thể tái sử dụng kiểm thử sinh thật, đồng thời nhấn mạnh sự khác biệt giữa cải thiện một bộ kiểm thử cụ thể và chứng minh hiệu quả tổng quát của thuật toán.

## 5.2. Hướng phát triển
Sau khi hoàn tất tập đánh giá bổ sung hiện có, hướng ưu tiên là bổ sung dự án độc lập và các phiên bản lỗi thực để kiểm tra khả năng chuyển giao. Việc chạy lại đúng benchmark của công trình gốc là một hướng đối chiếu riêng khi cần trả lời câu hỏi tái lập, không phải điều kiện để diễn giải kết quả của tập bổ sung. Trong thiết kế thành phần, cần tách ngữ cảnh phụ trợ, thiết lập và sửa lỗi thành các nhánh đối chứng có ngân sách tương đương. Với đánh giá toàn quy trình, cần đối chứng trực tiếp với Test4Py thay vì so các số tổng hợp khác phạm vi.

Nghiên cứu tiếp theo cũng cần tăng chất lượng thông tin thiết lập, rà soát cơ sở xác định kết quả mong đợi và dùng lỗi thực hoặc tập đột biến được chọn trước. Các thay đổi này nhằm chuyển từ tín hiệu cải thiện trong thực nghiệm thăm dò sang bằng chứng có độ tin cậy và phạm vi khái quát rõ ràng hơn.
