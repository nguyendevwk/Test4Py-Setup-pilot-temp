"""Prepare a new editorial layer without modifying earlier reports or evidence."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'research/editorial_v15';D.mkdir(exist_ok=True)
s=(R/'research/editorial_v14/report_body.md').read_text()
def section(start,end,new):
 global s
 a=s.index(start);b=s.index(end,a);s=s[:a]+new.strip()+'\n\n'+s[b:]
s=s.replace('## 1.3. Hướng cải tiến được khảo sát','## 1.3. Khoảng trống nghiên cứu và hướng cải tiến được khảo sát')
s=s.replace('Đóng góp được đánh giá ở mức thành phần và quy trình ứng dụng.', 'Khoảng trống được khảo sát là liệu thông tin sử dụng thu được với chi phí thấp có đủ giúp mô hình tạo kiểm thử khả dụng, khi không xây dựng phân tích ngữ nghĩa liên thủ tục toàn dự án. Đây là bài toán đánh đổi giữa mức thông tin, chi phí thu thập ngữ cảnh và độ tin cậy đầu ra. Bổ sung nhiều mã hơn có thể làm rõ phụ thuộc nhưng cũng tăng nhiễu; một cách khởi tạo chạy được có thể giảm lỗi đầu vào nhưng lại hướng mô hình về một số trạng thái hẹp. Vì vậy, lợi ích của ngữ cảnh phải được kiểm tra bằng đối chứng thành phần, không được giả định từ độ dài lời nhắc.\n\nĐóng góp được đánh giá ở mức thành phần và quy trình ứng dụng.')
section('## 3.1.','## 3.2.', '''## 3.1. Mô hình bài toán, mục tiêu và giả thuyết
Gọi f là đối tượng cần kiểm thử, M là mô-đun chứa f và E là môi trường thực thi đã cố định. Một chính sách ngữ cảnh lựa chọn thông tin từ M và các phép thử thiết lập để tạo C. Mô hình L nhận C cùng yêu cầu kiểm thử và sinh bộ T. Đầu ra nghiên cứu không chỉ là văn bản T mà còn là bằng chứng T được thu thập, thực thi và chạm tới phần thân f trong E. Mục tiêu thực nghiệm là tăng xác suất tạo bộ kiểm thử đáp ứng tiêu chí đã xác định, với ngân sách ngữ cảnh, đầu ra và sửa lỗi hữu hạn.

Mô hình bài toán phân biệt ba loại ràng buộc. Ràng buộc giao diện quyết định cách nhập và gọi đúng đối tượng. Ràng buộc trạng thái quyết định tiền điều kiện để hành vi có thể được thực thi. Ràng buộc ngữ nghĩa quyết định kết quả nào cần được khẳng định. Hai loại đầu chủ yếu liên quan tới tính khả thi của đầu vào; loại cuối liên quan tới test oracle. Phương pháp tác động trực tiếp vào hai loại đầu và cung cấp thêm bằng chứng mã nguồn cho loại cuối, nhưng không coi một lời gọi thử thành công là chứng minh kết quả mong đợi.

Ba nhánh dùng chung mô hình sinh và yêu cầu đầu ra. Nhánh A chỉ có mã đối tượng và các lệnh nhập. Nhánh B thêm thông tin thiết lập đã được thực thi thử khi có. Nhánh C giữ chính sách thiết lập của B và thêm khai báo phụ trợ có giới hạn. So sánh C với A trả lời câu hỏi hiệu quả chính sách kết hợp; B với A khảo sát thiết lập; C với B khảo sát giá trị tăng thêm của khai báo phụ trợ. Thiết kế chưa có nhánh chỉ khai báo phụ trợ nên không tách được đầy đủ tương tác giữa hai thành phần như một thiết kế nhân tố hai nhân hai.

@table hypotheses | Bảng 3.1. Giả thuyết cơ chế và bằng chứng dùng để đánh giá

Bảng giả thuyết hệ thống hóa lập luận nghiên cứu trong bản trình bày; các giả thuyết cơ chế không phải kết luận đã được xác nhận. Kế hoạch tương phản thống kê được cố định trước đợt lớn, còn các phân tích phân nhóm bổ sung ở Chương 4 là hậu kiểm mô tả.

@figure architecture | Hình 3.1. Quy trình sinh và đánh giá kiểm thử dựa trên ngữ cảnh và phản hồi thực thi

Nguồn: thiết kế của nghiên cứu. Trong đối chứng chính, số lượt sửa bằng không để đo hiệu quả ngữ cảnh ở lần sinh đầu; vòng phản hồi thuộc phạm vi đánh giá phát triển riêng.''')
section('## 3.2.','## 3.3.', '''## 3.2. Chính sách lựa chọn ngữ cảnh và xác nhận thiết lập
### 3.2.1. Khai báo phụ trợ theo quan hệ tham chiếu cục bộ
Ngữ cảnh cơ sở giữ khai báo đối tượng và các lệnh nhập của mô-đun. Phần mở rộng xem mỗi khai báo cấp mô-đun là một đỉnh; quan hệ từ khai báo u tới v tồn tại khi trong u có tên được đọc khớp với tên khai báo v trong cùng mô-đun. Mở rộng tối đa hai mức thu được phần giải thích cục bộ cho các hàm phụ trợ, lớp hoặc hằng số mà đối tượng sử dụng. Đây là quan hệ tham chiếu cú pháp, không phải đồ thị gọi đã phân giải đầy đủ: tên cục bộ trùng tên, truy cập thuộc tính, gọi động và phụ thuộc qua mô-đun khác có thể không được mô hình hóa chính xác.

Quy tắc giữ ngữ cảnh là xác định: xét tên theo thứ tự ổn định, không lặp lại khai báo đã xét và chỉ thêm khai báo nằm trong giới hạn. Mỗi khai báo phụ trợ tối đa 4.000 ký tự, tổng tối đa 8.000 ký tự; khai báo quá giới hạn bị bỏ qua thay vì cắt tùy ý giữa cấu trúc. Giới hạn ký tự là ràng buộc trích xuất, không tương đương giới hạn token của mô hình. Số token thực tế được đo từ phản hồi dịch vụ.

Lựa chọn mở rộng cục bộ nhằm giảm chi phí phân tích và giới hạn lượng thông tin không trực tiếp phục vụ đối tượng. Với mô-đun có n nút AST, một lượt duyệt thu thập khai báo có chi phí tỷ lệ với n; việc đọc lại tối đa hai mức vẫn bị chặn bởi kích thước nguồn và ngân sách trích xuất. Lập luận này mô tả tính chất của chính sách, không phải phép đo thời gian hoặc bằng chứng tối ưu. Đánh đổi là bỏ sót phụ thuộc liên mô-đun và không suy ra đầy đủ tiền điều kiện động.

### 3.2.2. Thiết lập như bằng chứng khả thi, không phải đáp án kiểm thử
Thông tin thiết lập xuất phát từ chữ ký và một chính sách đối số tối thiểu cố định. Tham số có mặc định được bỏ qua; tham số bắt buộc được gán ứng viên theo nhóm tên hoặc chú thích kiểu, gồm giá trị logic, danh sách rỗng, hàm gọi lại đơn giản hoặc giá trị số mặc định. Tham số chỉ nhận theo vị trí chưa được chính sách hỗ trợ. Chi tiết ứng viên được cố định trước khi sinh kiểm thử, không tìm kiếm lại theo kết quả đánh giá.

Mỗi phép thử có giới hạn 10 giây và chạy trong tiến trình riêng. Chỉ chữ ký và đối số của lời gọi hoàn tất mới đi vào ngữ cảnh; giá trị trả về và nội dung in ra của chương trình không được dùng làm đáp án. Với lớp, phép thử xác nhận một cách gọi hàm tạo; với hàm, nó xác nhận một lời gọi đã hoàn tất. Cả hai đều không chứng minh tính đại diện của dữ liệu hay tiền điều kiện của mọi phương thức.

@algorithm context | Thuật toán 3.1. Xây dựng ngữ cảnh theo chính sách cố định

Nếu không thu được gợi ý thiết lập hoặc khai báo phụ trợ, đối tượng vẫn được giữ ở nhánh đã chỉ định. Vì vậy, đại lượng được ước lượng là hiệu quả chính sách áp dụng trên toàn tập đủ điều kiện, gồm cả trường hợp không cung cấp thêm thông tin. Chỉ phân tích các phép thử thiết lập thành công sẽ đổi bài toán sang một tập đối tượng dễ hơn và làm mất tính tương ứng với thiết kế ban đầu.''')
section('## 3.3.','## 3.4.', '''## 3.3. Sinh kiểm thử và phản hồi có kiểm soát
Một bộ kiểm thử phải thể hiện ba phần: chuẩn bị trạng thái, kích hoạt hành vi và khẳng định thuộc tính quan sát được. Lời nhắc yêu cầu ba hàm kiểm thử cấp mô-đun, tập trung vào trường hợp thông thường, điều kiện biên hoặc ngoại lệ có căn cứ. Ba hàm là quy cách đầu ra chung, không bảo đảm mỗi hàm thuộc một loại hành vi cố định và không được xem là ba mẫu thống kê độc lập.

Ở đợt chính, số lần sửa bằng không. Lựa chọn này loại bỏ sự khác biệt về số cơ hội sửa và lượng phản hồi, để tương phản giữa các nhánh tập trung vào ngữ cảnh đầu vào. Đổi lại, tỷ lệ đạt phản ánh chất lượng sinh ở lần đầu dưới quy cách ba hàm, không phải khả năng tối đa của một hệ sinh kiểm thử có sửa lặp hoặc tích lũy độ phủ.

Trong phạm vi quy trình có phản hồi, kết quả thu thập và dấu vết ngoại lệ hỗ trợ mô hình sửa kiểm thử, tối đa hai lượt. Phân biệt lỗi giao diện, lỗi thiết lập và lỗi khẳng định giúp định hướng sửa, nhưng chưa có bằng chứng mọi lần sửa bảo toàn ý nghĩa. Vì vậy, thành công vận hành sau sửa và bảo toàn oracle là hai tiêu chí riêng. Các kết quả phát triển được dùng để hình thành giả thuyết về vai trò phản hồi, không thay thế đối chứng ngữ cảnh trên tập lớn.

@algorithm feedback | Thuật toán 3.2. Sinh và đánh giá với ngân sách sửa hữu hạn

Các lời nhắc tiếng Anh đã dùng được giữ ở Phụ lục 1. Bộ kiểm thử sinh ra được chạy trên mã sản phẩm đã cố định. Không sửa mã sản phẩm hoặc loại ca thất bại để thay đổi kết quả chấp nhận của một lượt đã lên lịch.''')
section('## 3.4.','## 3.5.', '''## 3.4. Định nghĩa chỉ số và đơn vị phân tích
Một lượt tương ứng với bộ ba đối tượng, nhánh và giá trị seed. Gọi A của lượt bằng 1 khi tất cả điều kiện chấp nhận thỏa mãn, bằng 0 khi đầu ra đã quan sát không thỏa. Các điều kiện gồm mã trích xuất được, đúng ba hàm kiểm thử cấp mô-đun, vượt kiểm tra cấu trúc, tất cả hàm được thu thập và các ca đều vượt qua, độ phủ mô-đun dương, có dòng thực thi thuộc phần thân đối tượng, đồng thời chạy lại đạt và khớp độ phủ dòng. Đối với lớp, chứng kiến một phần thân phương thức chưa chứng minh bao phủ tất cả phương thức.

@table metrics | Bảng 3.2. Chỉ số, mẫu số và giới hạn diễn giải

Với một nhánh, tỷ lệ theo lượt bằng tổng A chia cho 1.290 lượt. Với dự án p có n đối tượng và hai lượt lặp, tỷ lệ riêng bằng tổng A của dự án chia cho 2n. Tỷ lệ cân bằng dự án là trung bình của 21 tỷ lệ riêng. Quy tắc thứ nhất trả lời thu được bao nhiêu bộ đạt trong tập đang chạy; quy tắc thứ hai cho mỗi dự án cùng trọng số khi tổng hợp. Hai đại lượng có thể khác hướng thay đổi khi quy mô dự án không bằng nhau.

Độ phủ câu lệnh mô-đun bằng 100 nhân số dòng có thể thực thi đã được chạy chia cho tổng số dòng có thể thực thi. Độ phủ nhánh dùng số nhánh đã thực thi chia cho tổng số nhánh cần đo; không có nhánh thì ghi không áp dụng. Chỉ số độ phủ có tính lượt không đạt dùng tích A với độ phủ mô-đun của lượt, lấy trung bình theo dự án rồi trung bình giữa 21 dự án. Đây là chỉ số tổng hợp có phạt, không phải độ phủ thuần trên các bộ chạy thành công. Dữ liệu độ phủ thiếu vẫn được giữ là thiếu trong hồ sơ gốc.

Bằng chứng chạm thân đối tượng chỉ đòi hỏi giao giữa dòng thực thi và dòng trong thân hàm hoặc phương thức khác rỗng; nó ngăn ghi nhận chỉ nhập mô-đun mà không kích hoạt đối tượng. Không dùng điều kiện này để thay thế độ phủ mục tiêu hoặc chất lượng khẳng định. Tương tự, tỷ lệ chạy lại được tính trên các bộ đã được nhận, không phải trên toàn bộ 3.870 đầu ra.

Khảo sát ghép gói sử dụng mọi bộ đã nhận của một dự án và nhánh ở cả hai lượt lặp. Độ phủ gói được đo trên hợp các tệp nguồn thuộc danh mục đủ điều kiện của dự án, bao gồm tệp chưa được thực thi; không cộng các tỷ lệ độ phủ từng bộ. Chỉ số gói hợp lệ ghi nhận độ phủ khi toàn gói vượt qua và thu thập đủ ca, còn gói không đạt đóng góp bằng không khi tổng hợp 21 dự án. Mẫu số này khác độ phủ một mô-đun ở cấp lượt nên hai mức không được so trực tiếp như cùng một phép đo.

Kiểm thử đột biến báo cáo đồng thời số phát hiện, không phát hiện và chưa thể kết luận trên mẫu đã lên lịch. Chỉ ghi nhận phát hiện hành vi khi bộ kiểm thử vượt qua trên bản gốc và thất bại do kiểm tra hành vi trên bản biến đổi; lỗi thu thập hoặc hết thời gian không mặc nhiên được tính là phát hiện.''')
s=s.replace('@table design | Bảng 3.1.', '@table design | Bảng 3.3.')
needle='## 3.6. Phân tích thống kê và khả năng tái lập'
s=s.replace(needle,'''### 3.5.1. Môi trường, thành phần và tham số kiểm soát
@table environment | Bảng 3.4. Môi trường và thành phần thực nghiệm đã ghi nhận

Nguồn: cấu hình đã khóa, kiểm tra môi trường của 21 dự án và hồ sơ thực thi. Python 3.10.22, pytest 9.2.0, coverage.py 7.16.2 và pytest-json-report 1.5.0 được đối chiếu theo từng môi trường dự án. Có 2.020 tệp nguồn sản phẩm được kiểm tra khớp bản lưu; đây là kiểm tra tính nhất quán giữa quá trình chạy, không được mô tả thành kiểm tra trước suy luận nếu thời điểm không phù hợp. Phiên bản cụ thể của 21 gói được trình bày ở phụ lục.

Máy khách điều phối gửi yêu cầu tới Groq và thực thi kiểm thử trong các môi trường Python riêng của dự án. Phần cứng phục vụ suy luận của API không do nghiên cứu kiểm soát. Hồ sơ đợt lớn chưa đủ thông tin để công bố cấu hình CPU, RAM và hệ điều hành của máy khách tại thời điểm chạy như một cấu hình phần cứng đã khóa; vì vậy, nghiên cứu không dùng các phép đo này để khẳng định tốc độ suy luận hoặc so sánh phần cứng. Sự thiếu hụt thông tin làm hạn chế tái lập thời gian, dù mã nguồn, phụ thuộc, đầu ra và quy tắc đánh giá vẫn có thể đối chiếu.

Các tiến trình kiểm thử dùng thư mục làm việc và biến môi trường tối thiểu riêng; đây là cách ly tiến trình, không phải bảo đảm an toàn của hộp cát hệ điều hành. Giới hạn 20 giây là một phần định nghĩa đầu ra sử dụng được trong môi trường này. Khi tăng từ hai lên sáu tiến trình đánh giá đồng thời, tải máy có thể ảnh hưởng các ca gần ngưỡng thời gian; việc giữ nguyên thời hạn không đủ để chứng minh hoàn toàn loại bỏ tác động điều phối.

### 3.5.2. Kịch bản kiểm tra và quy tắc diễn giải
@table scenarios | Bảng 3.5. Ma trận kịch bản, biến thay đổi và kết quả cần quan sát

Các kịch bản hình thành một chuỗi bằng chứng: sinh được bộ khả dụng ở cấp đối tượng, kiểm tra khả năng chạy lại, ghép thành gói dự án và xem xét khả năng phát hiện thay đổi hành vi. Không yêu cầu kết quả mọi cấp cùng chiều. Khả năng chạy riêng tốt hơn nhưng ghép gói kém hơn sẽ dẫn tới kết luận cần cải thiện tính độc lập trạng thái, thay vì chọn một chỉ số thuận lợi làm đại diện toàn bộ chất lượng.

'''+needle)
s=s.replace('Với mỗi dự án, chênh lệch được tính trên các cặp đối tượng và lượt lặp, sau đó lấy trung bình giữa các dự án.', 'Với dự án p và tương phản C trừ A, đặt d(p) bằng tổng chênh lệch chấp nhận của các cặp đối tượng và seed chia cho số cặp của dự án. Hiệu ứng chính bằng tổng d(p) chia cho 21. Đơn vị hiệu ứng được báo theo điểm phần trăm, phân biệt với phần trăm tăng tương đối. Ghép cặp kiểm soát khác biệt đối tượng và tham số sinh, nhưng cùng seed qua API không bảo đảm hai nhánh có cùng chuỗi ngẫu nhiên nội bộ.')
# Consolidate historical exploration, preserving the full text in a dedicated appendix.
a=s.index('## 4.3.');b=s.index('## 4.4.',a);historic=s[a:b]
new='''## 4.3. Phân tích cơ chế và đánh đổi thiết kế
### 4.3.1. Đóng góp của thiết lập và khai báo phụ trợ
Thiết lập chỉ làm tăng số bộ đạt gộp từ 378 lên 383, trong khi tỷ lệ cân bằng dự án giảm 3,07 điểm phần trăm. Hai chỉ số trả lời câu hỏi khác nhau: số bộ thu được thiên về dự án có nhiều đối tượng, còn ước lượng cân bằng coi mỗi dự án là một đơn vị cùng trọng số. Sự khác biệt cho thấy không thể lấy tăng năm bộ làm bằng chứng thiết lập có lợi trên một dự án điển hình. Một lời gọi thiết lập tối thiểu có thể khả thi nhưng ít đại diện cho hành vi cần kiểm tra; đây là giả thuyết giải thích cần đối chứng thêm, chưa phải nguyên nhân được xác nhận.

Khi bổ sung khai báo phụ trợ trên cùng chính sách thiết lập, số bộ đạt tăng từ 383 lên 423. Thông tin cục bộ có thể giúp diễn giải giá trị hằng và quan hệ sử dụng, nhưng tác động quan sát còn bao gồm cách mô hình phản ứng với độ dài và cấu trúc ngữ cảnh. Chưa có đối chứng ngữ cảnh nhiễu cùng độ dài hoặc nhánh chỉ khai báo, nên không quy toàn bộ chênh lệch cho khả năng phân giải phụ thuộc của AST.

### 4.3.2. Kết quả ghép cặp và sự không đồng nhất
{{DEEP_PAIRED}}

@table paired | Bảng 4.3. Chuyển trạng thái chấp nhận trong các cặp cùng đối tượng và seed

Nguồn: phân tích mô tả hậu kiểm trên toàn bộ 1.290 cặp, không loại dự án hoặc seed theo kết quả. Bảng không tạo thêm phép kiểm định xác nhận ngoài kế hoạch đã khóa.

{{DEEP_SUBGROUP}}

### 4.3.3. Phản hồi sửa lỗi và phạm vi bằng chứng
Ở giai đoạn phát triển, cấu hình trước tinh chỉnh đạt 67/105 ngay lần sinh đầu và thêm 29 lượt sau sửa, gồm 24 ở vòng thứ nhất và 5 ở vòng thứ hai. Kết quả cho thấy phản hồi có thể tận dụng một phần đầu ra chưa đạt, nhưng chưa tách được tác động nhân quả của phản hồi khỏi các khác biệt cấu hình và lựa chọn đối tượng. Giai đoạn này có hướng dẫn theo thư viện và tinh chỉnh trên đối tượng đã quan sát; không được xem như xác nhận hiệu quả sửa lỗi trên tập 645 đối tượng.

Các khảo sát lựa chọn cấu hình và đối chứng nhỏ trước đợt lớn được gom vào Phụ lục 4. Việc rút gọn phần thân nhằm giữ mạch lập luận, không thay đổi kết quả, mẫu số hay loại các khảo sát bất lợi. Kết luận chính vẫn dựa trên toàn bộ đợt lớn, gồm cả đầu ra thất bại.

'''
s=s[:a]+new+s[b:]
# Remove distracting small recovery study from main, retaining exact content in appendix.
a=s.index('Phân tích thứ cấp trên khảo sát ban đầu');b=s.index('### 4.4.2.',a);recovery=s[a:b];s=s[:a]+s[b:]
s=s.replace('@table application | Bảng 4.5.', '@table application | Bảng 4.4.').replace('Bảng 4.6 so sánh','Bảng 4.5 so sánh').replace('@table efficiency | Bảng 4.6.','@table efficiency | Bảng 4.5.')
s=s.replace('Khả năng ghép các bộ được nhận thành gói chạy chung', 'Khả năng ghép các bộ được nhận thành gói chạy chung',1)
marker='### 4.4.2. Giá trị ứng dụng'
s=s.replace(marker,'''Kết quả tích hợp không cùng chiều kết quả sinh riêng: nhánh kết hợp có 423 bộ được nhận nhưng chỉ 17/21 gói vượt qua, so với 378 bộ và 20/21 gói của nhánh mã nguồn. Độ phủ gói hợp lệ cũng thấp hơn ở nhánh kết hợp. Hai mức sử dụng mẫu số và phạm vi nguồn khác nhau nên không có mâu thuẫn số học; chúng cho thấy tính khả dụng từng bộ chưa bảo đảm khả năng cùng tồn tại trong một tiến trình. Khác biệt trạng thái dùng chung, thứ tự chạy hoặc tài nguyên là các hướng cần điều tra, chưa được quy kết là nguyên nhân nếu chưa có đối chứng riêng. Khảo sát gói được bổ sung khi đang thu thập dữ liệu nên chỉ mang vai trò thăm dò.

'''+marker)
s=s.replace('## 4.6. Tổng hợp kết quả và giới hạn nghiên cứu','## 4.6. Tổng hợp bằng chứng và giới hạn suy luận')
s=s.replace('## 4.7. Giá trị thực tiễn của tập bổ sung và hướng mở rộng','## 4.7. Phương án cải tiến tiếp theo từ kết quả thực nghiệm')
needle='Đánh giá lỗi thực cũng là hướng bổ sung quan trọng.'
s=s.replace(needle,'''@table decisions | Bảng 4.6. Kết quả quan sát, phương án đề xuất và phép kiểm tra tiếp theo

Các phương án ở Bảng 4.6 là hướng nghiên cứu tiếp theo, chưa được tính vào kết quả cải tiến đã đo. Một chiến lược chọn ngữ cảnh thích ứng chỉ hợp lệ khi quy tắc được phát triển trên tập riêng và khóa trước khi đánh giá dự án mới; chọn nhánh tốt nhất sau khi xem nhãn từng đối tượng sẽ dùng thông tin không có ở thời điểm triển khai.

'''+needle)
(D/'historical_appendix.md').write_text(historic+'\n'+recovery)
(D/'report_body.md').write_text(s)
for name in ['full_benchmark_scope.json']:(D/name).write_bytes((R/'research/editorial_v14'/name).read_bytes())
(D/'editorial_plan.json').write_text(json.dumps({'previous':'v14','new':'v15','scope':'Research depth, operational metric definitions, environment, scenarios, posthoc descriptive analyses; no model calls','selection':'All3870 cases retained; historical exploratory studies moved intact to appendix without performance filtering','original_source_sha256':hashlib.sha256((R/'research/editorial_v14/report_body.md').read_bytes()).hexdigest()},ensure_ascii=False,indent=2))
print(D)
