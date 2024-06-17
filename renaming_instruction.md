모델링 스텝들이 사용할 네이밍 스크립트 개발

GUI
1. 에셋 이름 Textfield
2. Clean UP Button
3. export Button

# 에셋 name Textfield

에셋의 이름을 적는 칸.

# Clean Up Button

1. name textfield가 영어가 맞는 지 체크
2. 선택된 오브젝트 들을 FBX export 후 reimport. export data는 삭제.
   해당 기능은 Advanced skeleton에 있는 기능을 모방
3. name textfield의 정보를 가져와 group을 만듬 
4. group 내에 오브젝트 페어런트. 하면서 Renaming
    네이밍 방식은 아래와 같음
    if(name_textfield == chair1):
    group = AST_chair1_01
    child = chair1_head, chair1_wheel, chair1_body ... etc...   
    head, wheel 등의 데이터는 기존 오브젝트들에 지정되어 있는 네이밍에서 가져옴
--- 5번은 제가 할건데 도전해봐도 됨 ---
1. 메테리얼 이름 수정

# Export Button
1. group Select
2. FBX export - fileBrowserDialog 사용
   [fileBrowserDialog](https://download.autodesk.com/us/maya/2010help/commandspython/fileBrowserDialog.html)
3. 구글 드라이브 웹사이트 열건지 메시지 박스 - confirmDialog 사용
    [confirmDialog](https://download.autodesk.com/us/maya/2010help/CommandsPython/confirmDialog.html)
4. 구글드라이브 제출 웹사이트 열기
   [Gdrivelink](https://drive.google.com/drive/u/3/folders/1ye-1__vQbTPghiTcQXDgrZe72eBf3vqs)






