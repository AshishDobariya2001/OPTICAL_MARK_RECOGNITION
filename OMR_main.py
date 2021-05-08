import cv2
import numpy as np
import utlis
import os

score = 0
###########################################################
def Process(path, pre, fin, ans, questions, choice):
    print(path)
    widthImg = 700
    heightImg = 700
    # questions = 5
    # choice = 5
    # ans = [1, 2, 0, 1, 4]
    print(ans)
    ##################################
    # cap = cv2.VideoCapture(0)
    # cap.set(10, 150)
    ####################################

    img = cv2.imread(path)
    # PREPROSEESING
    img = cv2.resize(img, (widthImg, heightImg))
    imgContours = img.copy()
    imgFinal = img.copy()

    imgBiggestContours = img.copy()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 10, 50)

    # FIND ALL CONTOURS
    countours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(imgContours, countours, -1, (0, 255, 0), 10)
    try:
        # FIND RECTANGLES
        rectCon = utlis.rectCountour(countours)
        biggestContour = utlis.getCornerPoints(rectCon[0])
        # print(biggestContour.shape)
        gradePoints = utlis.getCornerPoints(rectCon[1])
        # print(biggestContour)

        if biggestContour.size != 0 and gradePoints.size != 0:
            cv2.drawContours(imgBiggestContours, biggestContour, -1, (0, 255, 0), 20)
            cv2.drawContours(imgBiggestContours, gradePoints, -1, (255, 0, 0), 20)

            biggestContour = utlis.reorder(biggestContour)
            gradePoints = utlis.reorder(gradePoints)

            pt1 = np.float32(biggestContour)
            pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
            matrix = cv2.getPerspectiveTransform(pt1, pt2)
            imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

            ptG1 = np.float32(gradePoints)
            ptG2 = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])
            matrixG = cv2.getPerspectiveTransform(ptG1, ptG2)
            imgGradeDisplay = cv2.warpPerspective(img, matrixG, (325, 150))
            # cv2.imshow("Grade",imgGradeDisplay)

            # APPLT THRESHOLD
            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
            imgThresh = cv2.threshold(imgWarpGray, 170, 255, cv2.THRESH_BINARY_INV)[1]

            boxes = utlis.splitBoxes(imgThresh)
            # cv2.imshow("Test",boxes[2])
            # print(cv2.countNonZero(boxes[1]),cv2.countNonZero(boxes[2]))

            # GETTING NONE ZERO PIXEL VALUE EACH BOXES
            myPixelVal = np.zeros((questions, choice))  # row and column
            countC = 0
            countR = 0

            for image in boxes:
                totolPixels = cv2.countNonZero(image)
                myPixelVal[countR][countC] = totolPixels
                countC += 1
                if (countC == choice): countR += 1;countC = 0  # choice pixel fatch throw this code
            # print(myPixelVal)

            # FINDING INDEX VALUES OF THE MARKINGS
            myIndex = []
            for x in range(0, questions):  # all pixel is convert into row like Q1: A B C D E
                arr = myPixelVal[x]
                # print("arr",arr)
                myIndexVal = np.where(arr == np.amax(arr))  # frist row to find max value thresold this answer of Q:1
                # print(myIndexVal[0])
                myIndex.append(myIndexVal[0][0])  # list of Answer
            # print(myIndex)

            # GRADING
            grading = []
            for x in range(0, questions):
                if (ans[x] == myIndex[x]):
                    grading.append(1)  # perform array of grade[1,1,1,1,1,1]
                else:
                    grading.append(0)
            # print(grading)
            global score
            score = (sum(grading) / questions) * 100  # FINAL GRADE            # count final grade
            print(score)

            # DISPLAYING ANSWERS
            imgResult = imgWarpColored.copy()
            imgResult = utlis.showAnswer(imgResult, myIndex, grading, ans, questions, choice)
            imgRawDrawing = np.zeros_like(imgWarpColored)
            imgRawDrawing = utlis.showAnswer(imgRawDrawing, myIndex, grading, ans, questions, choice)
            invMatrix = cv2.getPerspectiveTransform(pt2, pt1)
            imgInvWarp = cv2.warpPerspective(imgRawDrawing, invMatrix, (widthImg, heightImg))

            imgRawGrade = np.zeros_like(imgGradeDisplay)
            cv2.putText(imgRawGrade, str(int(score)) + "%", (60, 100), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 255, 255), 3)
            # cv2.imshow("Grade",imgRawGrade)
            InvMatrixG = cv2.getPerspectiveTransform(ptG2, ptG1)
            imgInvGradeDisplay = cv2.warpPerspective(imgRawGrade, InvMatrixG, (widthImg, heightImg))

            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp, 1, 0)
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvGradeDisplay, 1, 0)

        imgBlank = np.zeros_like(img)

        imageArray = ([img, imgGray, imgBlur, imgCanny],
                      [imgContours, imgBiggestContours, imgWarpColored, imgThresh],
                      [imgResult, imgRawDrawing, imgInvWarp, imgFinal])
    except:
        imgBlank = np.zeros_like(img)
        imageArray = ([img, imgGray, imgBlur, imgCanny],
                      [imgBlank, imgBlank, imgBlank, imgBlank],
                      [imgBlank, imgBlank, imgBlank, imgBlank])

    lables = [["Orignal", "Gray", "Blur", "Canny"],
              ["contours", "biggestContours", "Warp", "Thresold"],
              ["Result", "Raw Drawing", "Inv Warp", "Final Img"]]

    imagStacked = utlis.stackImages(imageArray, 0.35, lables)
    if (pre == 1):
        cv2.imshow("Stacked Image", imagStacked)

    if (fin == 1):
        cv2.imshow("Fianl Result", imgFinal)

    path = 'E:/Project/mini_project/venv/ImageFile'
    cv2.imwrite(os.path.join(path, 'FinalOutput.jpg'), imgFinal)
    cv2.waitKey(0)


def Score():
    print(score)
    return score
