import os

def create_folders(names_list, base_directory):
    for name in names_list:
        folder_path = os.path.join(base_directory, name)
        try:
            os.makedirs(folder_path)
            print(f"폴더 생성 완료: {folder_path}")
        except FileExistsError:
            print(f"폴더 이미 존재함: {folder_path}")
        except Exception as e:
            print(f"폴더 생성 실패: {folder_path}. 오류: {str(e)}")

# 예제 리스트와 기본 디렉토리 설정
name_list = [
    "Ray Gun (광선총)",
    "Hook Gun (갈고리총)",
    "Turtle Gun (거북이총)",
    "Water Gun (물총)",
    "Electric Gun (전기총)",
    "Lego Mine Gun (레고지뢰총)",
    "Fire Sword (불검)",
    "Ultrasonic Bracelet (초음파 팔찌)",
    "EMP Gloves (EMP 장갑)",
    "Jam Knife-Shaped Sword (잼칼모양검)",
    "Sticky Shooter (끈적이발사총)",
    "Weapon Display Wall (무기전시벽)",
    "Frame (액자)",
    "Sadness Bomb (슬픔폭탄)",
    "Anger Bomb (화남폭탄)",
    "Dizziness Bomb (어지러움폭탄)",
    "Madness Bomb (광기폭탄)",
    "Dynamite (다이너마이트)",
    "Sofa (소파)",
    "CCTV Clothes Hanger (CCTV 옷걸이)",
    "Vending Machine (자판기)",
    "Drawer (서랍장)",
    "Wall-Mounted Machines (벽에 붙은 기계들)",
    "Energy Tank (에너지탱크)",
    "Stainless Steel Container (스테인리스 통)",
    "Robot Flower (로봇꽃)",
    "Flower Pot (화분)",
    "Wall Shelf (벽걸이 선반)",
    "Clock (시계)",
    "Door (문)",
    "Small Frame 1 (소형 액자1)",
    "Small Frame 2 (소형 액자2)",
    "Sleeping/Working Signs (자는중 일하는중 등)",
    "Bookshelf with Drawers (책서랍장)",
    "Book (책)",
    "Globe (지구본)",
    "Ladder (사다리)",
    "Erlenmeyer Flask (삼각 플라스크)",
    "Round Flask (둥근 플라스크)",
    "Distillation Flask (증류 플라스크)",
    "Beaker (비커)",
    "Test Tube + Rack (시험관+시험관대)",
    "Tripod (삼발이)",
    "Alcohol Lamp (알코올램프)",
    "Mortar and Pestle (막자사발+막자)",
    "Spray Bottle (분무기)",
    "Ring Stand + Test Tube (링스탠드+시험관)",
    "U-Tube (U자관)",
    "Funnel (깔때기)",
    "Pipette (피펫(스포이드))",
    "Electronic Scale (전자저울)",
    "Toolbox (도구상자)",
    "Petri Dish (패트리 접시)",
    "Box + Sundries (박스+잡동사니)",
    "Document Box (서류 박스)",
    "Open Box (열린 박스)",
    "General Box (일반 박스)",
    "Potion Storage Drawer (물약 보관 서랍장)",
    "Stand Lamp (스탠드 전등)",
    "Power Strip (멀티탭)",
    "Operation Wall (작전벽)",
    "Printer (프린트기)",
    "Projector (영상기)"
]
  # 여기에 원하는 이름 리스트 추가
base_directory = "D:/GraduationHijackers/내 드라이브/Assets"  # 여기에 기본 디렉토리 경로 입력

create_folders(name_list, base_directory)
