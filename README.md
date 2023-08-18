# Scout Camera Simulation

## 목표 
- Scout_mini에 카메라를 달아서 Line_Detect 후 선 안에서 자율주행을 한다.
    - 중요 기술 
    1. Bird Eye
    2. White and Yello Line Sepertaion
    3. Image Blend and Binary Line
    4. Sliding Window to help following Line
    5. Line Keeping Assit System Algorithm

### 들어가기전 RosBag
- rosbag은 ros의 모든 토픽과 데이터를 저장해서 프로그램을 실행시키지 않아도 데이터를 송신해서 실제 현장 실험의 횟수를 줄일수 있는 도구
- rosbag record -a 를 하면 데이터를 저장
- rosbag play <플레이하고싶은 파일> 를 하면 저장된 데이터가 실행된다
- play했을때 보고싶은 데이터는 rostopic 이나 rviz, rqt를 사용하면 됨

<img src="./image/rosbag.gif" width="600px" height="400px">


### Bird Eye
- 카메라는 전면을 봐서 차선을 온전히 인식하지 못함
- 그렇기에 차선을 위-> 아래로 보도록 이미지를 수정해야 라인 인식이 쉬움
- 일정 영역을 Projection 시켜서 차선을 수직으로 볼수 있게 해야함

<img src="./image/bird_eye.gif" width="600px" height="400px">
---

### Yellow & White Detect
- 차선을 따라가게 주행하려면 주행할 수 있는 영역과 경계선을 파악해야함
- OpenCv2의 내부 메소드 rgbtohsv로 채도(hue)값을 이용해서 영역을 설정
- 원하는 색깔의 영역을 bitand 연산해서 색이 있는 부분만 남김



### Blend & Binary Calculation
- 차선 두개를 인식한 뒤 차선 주행을 원활하게 하기 위해서 차선을 이진화 시킨다
    - 차선(노란색 또는 하얀색) = 1(흰색)
    - 다른곳 = 0(검정)

<img src="./image/binary.gif" width="600px" height="400px">
