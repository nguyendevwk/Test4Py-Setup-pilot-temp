"""Prepare research narrative templates; completed evidence required to fill numbers."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];s=(R/'research/editorial_v12/report_body.md').read_text()
def replace_section(text,start,end,new):
 a=text.index(start);b=text.index(end,a);return text[:a]+new.strip()+'\n\n'+text[b:]
s=s.replace('RQ1. Việc bổ sung thông tin thiết lập đã được thực thi thử có cải thiện tỷ lệ bộ kiểm thử đạt yêu cầu và độ phủ so với chỉ cung cấp mã nguồn trên nhiều dự án hay không?','RQ1. Ngữ cảnh có giới hạn kết hợp thông tin thiết lập đã được thực thi thử có cải thiện tỷ lệ bộ kiểm thử đạt yêu cầu và độ phủ so với chỉ cung cấp mã nguồn trên nhiều dự án hay không?')
s=s.replace('RQ2. Ngữ cảnh mã nguồn và phản hồi thực thi đóng góp như thế nào vào quá trình sinh và sửa kiểm thử?','RQ2. Thông tin thiết lập, khai báo phụ trợ và phản hồi thực thi đóng góp như thế nào vào quá trình sinh và sửa kiểm thử?')
s=s.replace('Phạm vi thực nghiệm gồm giai đoạn phát triển trên 21 đối tượng; hai đợt đánh giá thành phần trên 27 đối tượng thuộc 9 dự án và 34 đối tượng thuộc 12 dự án; cùng các khảo sát bổ trợ về ngữ cảnh, sửa lỗi và ngân sách đầu ra.','Đánh giá trọng tâm bao phủ toàn bộ 645 đối tượng đủ điều kiện trên 169 mô-đun thuộc 21 dự án trong danh mục hiện có. Ba cấu hình ngữ cảnh và hai lượt lặp tạo 3.870 lượt đánh giá. Giai đoạn phát triển trên 21 đối tượng, hai đợt đối chứng nhỏ hơn và các khảo sát vận hành được giữ làm bằng chứng bổ trợ.')
s=replace_section(s,'## 3.5. Thiết kế thực nghiệm và vai trò của các tập dữ liệu','## 3.6. Phân tích thống kê và khả năng tái lập','''## 3.5. Thiết kế thực nghiệm trên toàn bộ phạm vi đủ điều kiện
Đánh giá chính sử dụng toàn bộ 645 hàm hoặc lớp đáp ứng tiêu chí nguồn mã trong các danh mục đã lưu. Các đối tượng thuộc 169 mô-đun và 21 dự án; không chỉ giữ vài trường hợp đại diện. Danh sách, phiên bản môi trường, lời nhắc, số lượt lặp và kế hoạch phân tích được cố định trước khi gọi mô hình cho đợt này.

Ba nhánh được so sánh ghép cặp gồm chỉ mã nguồn, mã nguồn kèm thiết lập đã thử, và mã nguồn kèm cả thiết lập lẫn khai báo phụ trợ. Mỗi đối tượng có hai lượt lặp, với giá trị seed 71 và 72 được gửi qua API. Cả ba nhánh sử dụng GPT-OSS-20B, nhiệt độ 0,2, giới hạn 2.048 token đầu ra và không sửa lỗi, tạo tổng cộng 3.870 lượt, tương ứng 1.290 lượt mỗi nhánh. Việc ưu tiên ba cấu hình giúp đánh giá đóng góp thành phần trên cùng tập đối tượng; số lượt lặp không thay thế số dự án độc lập.

@table design | Bảng 3.1. Thiết kế đánh giá chính và các nguồn bằng chứng bổ trợ

Thông tin thiết lập dùng được ở 337/645 đối tượng; phần khai báo phụ trợ có ở 388/645 đối tượng. Khi không có một loại thông tin bổ sung, đối tượng vẫn được giữ trong mẫu đánh giá và nhánh tương ứng dùng phần ngữ cảnh còn lại. Tương phản vì vậy đo hiệu quả của một chính sách bổ sung thông tin khi có thể thu được, không giả định mọi đối tượng đều có gợi ý hoàn hảo.

Điều kiện đủ tiêu chí được xác định từ nguồn mã trước suy luận: khai báo công khai ở cấp mô-đun, dài từ 5 đến 160 dòng và phần khai báo đối tượng không quá 6.000 ký tự. Các mô-đun được lấy theo danh mục liên quan tới Test4Py và CodaMOSA [1], [23], với phiên bản package được khóa theo môi trường đã ghi nhận. Việc phủ toàn bộ danh mục đủ điều kiện này không đồng nghĩa tái lập nguyên phiên bản hoặc toàn bộ mô-đun của hai benchmark gốc.

Các nhánh chạy luân phiên trong từng cặp đối tượng và lượt lặp. Kiểm thử được thực thi trong tiến trình riêng, dùng môi trường phụ thuộc của dự án và cùng giới hạn thời gian 20 giây mỗi lần chạy. Đầu ra phải có đúng ba hàm kiểm thử cấp mô-đun; cả ba hàm phải được pytest thu thập và chạy thành công. Các trường hợp tham số hóa được tính là các ca trong ba hàm này, không phải đối tượng thống kê mới.

Trong 645 đối tượng, 61 đã được dùng ở hai đợt đối chứng chuẩn hóa trước, còn 584 chưa nằm trong hai tập đối chứng đó. Tuy nhiên, cả 21 dự án đều đã được quan sát trong quá trình triển khai. Đợt này đánh giá độ bao quát trong khung đã xác định, không được gọi là xác nhận trên 21 dự án hoàn toàn mới. Các số liệu cũ không được cộng vào 3.870 lượt của đối chứng chính.''')
s=replace_section(s,'## 3.6. Phân tích thống kê và khả năng tái lập','# CHƯƠNG 4. THỰC NGHIỆM VÀ ĐÁNH GIÁ','''## 3.6. Phân tích thống kê và khả năng tái lập
Tương phản chính đã khóa là nhánh ngữ cảnh kết hợp thiết lập trừ nhánh chỉ mã nguồn. Hai tương phản phụ là thiết lập trừ mã nguồn và ngữ cảnh kết hợp trừ thiết lập. Tương phản phụ thứ hai đo phần giá trị bổ sung của khai báo phụ trợ khi giữ cùng chính sách thiết lập.

Với mỗi dự án, chênh lệch được tính trên các cặp đối tượng và lượt lặp, sau đó lấy trung bình giữa các dự án. Báo cáo đồng thời trình bày tỷ lệ theo lượt để mô tả số bộ kiểm thử sử dụng được và tỷ lệ cân bằng dự án để phân tích khả năng chuyển giao. Độ phủ có tính lượt không đạt cũng được báo theo cùng cách cân bằng khi dùng cho đánh giá chính.

Khoảng tin cậy 95% sử dụng 20.000 lần lấy mẫu lại theo cụm dự án, với giá trị khởi tạo 20261119. Kiểm định đổi dấu hai phía được tính ở cấp 21 dự án. Phép kiểm định cần giả định độc lập và khả năng hoán đổi dấu của chênh lệch dưới giả thuyết không; việc ghép cặp tự nó không bảo đảm các giả định này. Hai giá trị p của các tương phản phụ được hiệu chỉnh bằng phương pháp Holm; tương phản chính được xác định riêng trước chạy. Các khoảng tin cậy là khoảng biên cho từng tương phản, không phải khoảng đồng thời.

Phân tích kết luận chỉ được thực hiện khi có đủ toàn bộ tích các đối tượng, ba nhánh và hai lượt lặp. Không dừng nghiên cứu khi thấy kết quả thuận lợi. Mọi đầu ra mô hình không đạt tiêu chí vẫn nằm trong mẫu số. Sự cố truyền thông, bằng chứng hỏng hoặc nguồn mã bị thay đổi làm tạm dừng để đối chiếu, không bị chuyển thành một kết quả chất lượng mô hình đã quan sát.

Mỗi lượt lưu lời nhắc, đầu ra mô hình, mã kiểm thử và kết quả thực thi. Các bộ được nhận còn được chạy lại độc lập. Chạy lại đầu ra đã lưu và tính lại thống kê là hai mức tái lập có thể kiểm tra trực tiếp. Sinh mới qua API là một mức khác, chịu ảnh hưởng của dịch vụ và phiên bản mô hình cung cấp.''')
s=replace_section(s,'## 4.1. Tổ chức đánh giá theo câu hỏi nghiên cứu','## 4.3. Vai trò của ngữ cảnh và phản hồi sửa lỗi','''## 4.1. Tổ chức đánh giá theo câu hỏi nghiên cứu
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

Tương phản thiết lập so với mã nguồn là {{SETUP_DIFF}} điểm phần trăm, với p đã hiệu chỉnh {{SETUP_HOLM}}. Khi giữ cùng thông tin thiết lập và bổ sung khai báo phụ trợ, chênh lệch là {{CLOSURE_DIFF}} điểm phần trăm, với p đã hiệu chỉnh {{CLOSURE_HOLM}}. Hai kết quả này giúp phân biệt phần giá trị của thiết lập với phần giá trị của khai báo phụ trợ, thay vì quy toàn bộ kết quả cho AST.

@figure effects | Hình 4.1. Hiệu ứng của phương pháp và hai tương phản thành phần theo dự án

Nguồn: phân tích cụm của đợt đánh giá đầy đủ. Mốc không trên trục hoành biểu thị hai nhánh có cùng tỷ lệ đạt. Các khoảng là khoảng tin cậy biên 95%.

Phân bố kết quả của toàn bộ 21 dự án được trình bày tại Phụ lục 2. Kết quả có thể khác nhau theo kiểu giao diện và mức thông tin bổ sung thu được; số đối tượng lớn không làm các dự án trở thành mẫu ngẫu nhiên của mọi phần mềm Python. Đợt toàn phạm vi làm rõ mức độ bao quát trong khung đã cố định, còn khả năng khái quát ra các dự án mới vẫn cần đánh giá riêng.

RQ1 được trả lời theo phạm vi tương phản chính và khoảng bất định đã báo. RQ2 về đóng góp thiết lập và khai báo phụ trợ được đánh giá bằng hai tương phản phụ cùng dữ liệu, thay vì chọn một tập con có kết quả tốt hơn.''')
# Insert small earlier evaluations as one historical reference, not competing primary cohorts.
anchor='## 4.4. Chất lượng kiểm thử và nghiên cứu ứng dụng 14B'
extra='''### 4.3.3. Đối chiếu với các đợt đánh giá trước khi mở rộng toàn phạm vi
Hai đợt đối chứng trước ghi nhận 28/81 so với 36/81 lượt đạt trên 9 dự án, và 32/102 so với 34/102 trên 12 dự án khi bổ sung thiết lập. Chênh lệch cân bằng dự án lần lượt là 9,88 và 1,85 điểm phần trăm; cả hai khoảng tin cậy còn chứa không. Đây là bối cảnh phát triển dẫn tới nhu cầu đánh giá toàn bộ danh mục, không được cộng vào số lượt của đợt chính mới.

Bảng chi tiết của hai đợt được giữ ở phụ lục để đối chiếu. Bốn dự án trong đợt 12 dự án từng xuất hiện ở tập phát triển lịch sử. Phân tích hậu kiểm trên tám dự án còn lại có 19/72 và 24/72 lượt đạt, với khoảng tin cậy chênh lệch còn chứa không; kết quả này cũng không thay thế mẫu đầy đủ.

'''
s=s.replace(anchor,extra+anchor)
s=s.replace('Trong hai tập đối chứng chính, 64 bộ kiểm thử được nhận ở tập 9 dự án và 66 bộ ở tập 12 dự án đều chạy lại thành công, với độ phủ khớp kết quả đã lưu. Khảo sát ngữ cảnh phụ trợ có thêm 23 bộ được nhận và cả 23 bộ cũng chạy lại thành công.','Trong đợt toàn phạm vi, có {{ACCEPTED_TOTAL}} bộ được nhận theo tiêu chí thực thi và chạy lại của quy trình. Kiểm tra độc lập tiếp theo chạy lại {{REPLAY_COUNT}} bộ: {{REPLAY_PASSED}} bộ vượt qua và {{REPLAY_MATCHED}} bộ khớp độ phủ đã lưu. {{REPLAY_INTERPRETATION}} Hai đợt đối chứng trước có 64 và 66 bộ được nhận đều chạy lại thành công; khảo sát phụ trợ cũ có thêm 23 bộ với cùng kết quả kiểm tra.')
s=s.replace('Sổ theo dõi API ghi 688 phản hồi có thông tin sử dụng, với chi phí ước tính theo đơn giá cấu hình là 0,158223 USD. Tổng phân bổ bảo thủ là 0,605180 USD, gồm các khoản đặt trước và đối soát mốc ban đầu, nằm trong trần 3 USD.','Sau đợt toàn phạm vi, sổ theo dõi API ghi {{SETTLED_RESPONSES}} phản hồi có thông tin sử dụng, với chi phí ước tính theo đơn giá cấu hình là {{SETTLED_COST}} USD. Tổng phân bổ bảo thủ là {{ACCOUNTED_COST}} USD, gồm các khoản đặt trước và đối soát mốc ban đầu, nằm trong trần 3 USD. Riêng đợt toàn phạm vi có chi phí sử dụng ước tính {{FULL_COST}} USD.')
s=s.replace('Các phản hồi có sử dụng được ghi nhận với trạng thái HTTP 200; lịch gọi được điều tiết theo hạn mức dịch vụ.','Lịch gọi được điều tiết theo hạn mức dịch vụ; mọi sự cố và khoản đặt trước chưa quyết toán được giữ trong sổ theo dõi.')
s=replace_section(s,'## 4.6. Tổng hợp kết quả và giới hạn nghiên cứu','## 4.7. Mở rộng đánh giá toàn bộ phạm vi benchmark','''## 4.6. Tổng hợp kết quả và giới hạn nghiên cứu
Đợt toàn phạm vi mở rộng bằng chứng từ vài đối tượng được chọn sang toàn bộ 645 đối tượng đủ điều kiện trong danh mục. Ba nhánh và hai lượt lặp được áp dụng theo cùng một thiết kế trên 21 dự án, giúp đánh giá phương pháp và thành phần trong một mạch thống nhất. {{PRIMARY_INTERPRETATION}} Phạm vi kết luận vẫn là chính sách cung cấp ngữ cảnh trong môi trường và tiêu chí đã xác định, không phải ưu thế so với toàn bộ Test4Py.

Về tính hợp lệ của phép đo, chạy thành công và độ phủ không thay thế cơ sở xác định kết quả mong đợi. Chạy lại xác nhận sự nhất quán trong môi trường được kiểm tra; khảo sát đột biến nhỏ chỉ kiểm tra một phần độ nhạy hành vi. Các khảo sát đột biến lịch sử sử dụng bộ kiểm thử tuyển chọn nên được phân biệt với kết quả sinh kiểm thử của đợt toàn phạm vi.

Về tính hợp lệ nội tại, quy tắc ngữ cảnh và phân tích của đợt mới được khóa trước suy luận. Tuy nhiên, các dự án đã được quan sát và 61 đối tượng từng tham gia đối chứng trước. Giai đoạn phát triển cũ còn có hướng dẫn theo thư viện, ví dụ điều kiện khẳng định và tinh chỉnh trên đối tượng đã quan sát. Nghiên cứu giữ các bằng chứng phát triển này riêng, không coi là xác nhận khả năng tự xây dựng kết quả mong đợi trên dự án chưa biết.

Về kết luận thống kê, số lượt tăng lên 3.870 không tạo ra 3.870 dự án độc lập. Phân tích vẫn dựa trên 21 cụm dự án với các giả định đã nêu. Phiên bản package và phạm vi đủ tiêu chí cũng khác benchmark gốc. Chưa có đối chứng toàn quy trình với Test4Py trên cùng điều kiện; độ phủ cao hoặc một tương phản có ý nghĩa thống kê không tự cung cấp đối chứng đó.''')
s=replace_section(s,'## 4.7. Mở rộng đánh giá toàn bộ phạm vi benchmark','# CHƯƠNG 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN','''## 4.7. Phạm vi đã bao phủ và hướng mở rộng benchmark gốc
Nghiên cứu đã hoàn tất đánh giá toàn bộ 645 đối tượng đủ điều kiện trong danh mục hiện có, thay vì chỉ trình bày một số trường hợp nhỏ. Khái niệm toàn phạm vi trong báo cáo gắn với 169 mô-đun và 21 dự án có môi trường nguồn mã phù hợp; nó không có nghĩa mọi mô-đun của benchmark Test4Py gốc hoặc mọi cấu hình hệ thống đều đã được chạy.

Để khẳng định cải tiến so với Test4Py, bước tiếp theo cần cố định đúng phiên bản benchmark và chạy cả hai quy trình trên cùng đối tượng, mô hình hoặc ngân sách tương đương, số lần sửa và môi trường. Chạy thêm nhiều đối tượng trong các dự án đã quan sát giúp làm rõ hiệu quả trong phạm vi đó; bổ sung dự án hoàn toàn mới mới trực tiếp mở rộng số cụm kiểm tra khả năng khái quát.

Đánh giá lỗi thực cũng là hướng bổ sung quan trọng. Có thể sử dụng cặp phiên bản lỗi và đã sửa trong BugsInPy [24], giữ bộ kiểm thử chuẩn ngoài lời nhắc và chỉ ghi nhận phát hiện khi kiểm thử chạy đúng trên bản đã sửa nhưng nhận biết được sai lệch trên bản có lỗi. Các mở rộng này phục vụ câu hỏi nghiên cứu đã xác định, không nhằm tìm tập con thuận lợi hoặc bảo đảm trước một giá trị p.''')
s=s.replace('Hai đối chứng nhiều dự án cho thấy mức tăng quan sát của chính sách thiết lập lần lượt là 9,88 và 1,85 điểm phần trăm khi cân bằng theo dự án. Khoảng tin cậy của cả hai còn chứa không. Dữ liệu chưa đủ để xác nhận ưu thế thống kê hoặc vượt phương pháp Test4Py đầy đủ.','Đối chứng toàn phạm vi hoàn tất 3.870 lượt trên 645 đối tượng thuộc 21 dự án. Tương phản chính giữa ngữ cảnh kết hợp và mã nguồn là {{PRIMARY_DIFF}} điểm phần trăm, với khoảng tin cậy 95% từ {{PRIMARY_LO}} đến {{PRIMARY_HI}} điểm. {{PRIMARY_INTERPRETATION}} Dữ liệu chưa cung cấp đối chứng toàn quy trình để khẳng định vượt Test4Py đầy đủ.')
s=s.replace('Hướng ưu tiên là đánh giá toàn bộ đối tượng đủ điều kiện trong một khung benchmark cố định, đồng thời bổ sung dự án độc lập để kiểm tra khả năng chuyển giao.','Sau khi hoàn tất khung đủ điều kiện hiện có, hướng ưu tiên là mở rộng tới đúng phiên bản benchmark gốc và bổ sung dự án độc lập để kiểm tra khả năng chuyển giao.')
# Shift development tables to make room for the full-scope contrast table.
for n in range(5,1,-1):s=s.replace('Bảng 4.'+str(n), 'Bảng 4.'+str(n+1))
# The newly inserted contrast table was already numbered 4.2; restore only its directive.
s=s.replace('@table contrasts | Bảng 4.3. Chênh lệch ghép cặp','@table contrasts | Bảng 4.2. Chênh lệch ghép cặp')
description=R/'research/groq_full_scope_20261119/dataset_description.json'
if description.exists():
 import json
 d=json.loads(description.read_text());line=d['source_lines'];kind=d['types'];s=s.replace('Thông tin thiết lập dùng được ở 337/645 đối tượng;',f"Tập đối tượng gồm {kind['function']} hàm và {kind['class']} lớp. Độ dài khai báo trung vị là {line['median']:g} dòng, với khoảng tứ phân vị từ {line['q1']:g} đến {line['q3']:g} dòng; tiêu chí chọn nguồn mã vì vậy cần được xét khi khái quát tới các lớp lớn hơn hoặc hệ thống tích hợp.\n\nThông tin thiết lập dùng được ở 337/645 đối tượng;")
(R/'research/editorial_v13/report_body.template.md').write_text(s)
print('Prepared full-scope narrative template; final numbers are unresolved by design')
if __name__=='__main__':pass
