from deepface import DeepFace
from PIL import Image
import numpy as np
from os import system, remove, listdir, mkdir
from tqdm import tqdm
import traceback
from time import sleep
import imageio

class AudienceAnalyzer:
    # init method or constructor
    def __init__(self):
        try: 
            remove("./img_final/representations_facenet.pkl")   #For fresh start
        except:
            pass


    def SplitFrames(self):
        # -r (int) is fps value
        system("""ffmpeg -hwaccel cuda -i "video.mp4" -r 1 img_src/%01d.jpg""") #ffmpeg to split video frames

    def ListFiles(self, id=False):
        if id:
            path = f"website/static/data/{id}/"
            return listdir(f"{path}img_final")
        else:
            return listdir("./img_final")

    def SaveFaces(self, id=False):
        if id:
            path = f"website/static/data/{id}/"
        else:
            path = "./"
        for i in tqdm (range(1, len(listdir(f"{path}img_src"))), desc="Extracting"):

            try:

                #Getting Face List
                try:
                    img_list = DeepFace.extract_faces(img_path=f"{path}img_src/{str(i)}.jpg", enforce_detection=False, align=False)
                except:
                    continue

                #Check for if list is empty
                if img_list is None or len(img_list) == 0:
                    continue
                
                #Loop for all images in list
                s=0
                for img in img_list:
                    s+=1
                    #Confidence Filter
                    if img['confidence'] < 2:
                        continue

                    face = img['face']
                    img_final = Image.fromarray(np.uint8(255 * face)) #Generating image from array
                    #img_final.save(f"./img_final/{str(img['confidence'])}.png")
                    img_final.save(f"{path}img_final/{str(i)}_{str(s)}.jpg") #Saving Face Image
                    #print(img['confidence'])

            except Exception as e: #Error handling.
                if str(e).startswith("No"):
                    break
                elif str(e).startswith("Face"):
                    pass
                else:
                    print(e)
                    print(traceback.format_exc())

        print("Extraction Complete.")

    def CloneFinder(self, base_face, id=False):
        if id:
            path = f"website/static/data/{id}/"
        else:
            path = "./"
        # Search for all clones in folder
        clone_list = DeepFace.find(img_path = base_face, db_path = f"{path}img_final", model_name="Facenet", enforce_detection=False, align=False, silent=True)
        clone_names = clone_list[0]['identity']     

        return clone_names
    
    def CloneRemover(self, clone_names, base_face, id=False):
        if id:
            path = f"website/static/data/{id}/"
        else:
            path = "./" 
        #Removes all clones except base image
        for i in clone_names:
            if i != base_face:
                remove(i)
            else:
                continue

    def AnalyzeFace(self, base_face, silent=False, id=False):
        if id:
            path = f"website/static/data/{id}/"
        else:
            path = "./" 
        #Analyzing face attributes
        if str(base_face)[0].isdigit():
            base_face = f"{path}img_final/{base_face}"

        face_result = DeepFace.analyze(img_path = base_face, 
        actions = ['age', 'gender', 'race', 'emotion'], enforce_detection=False, align=False, silent=True)
        with open(f'website/static/data/{id}/report.csv','a') as csvfile:
            np.savetxt(csvfile,[["age", "age_text", "gender", "race", "emotion","file_name"]],delimiter=',',fmt='%s', comments='')

        for i in face_result:

            age = int(i['age'])
            gender = str(i['dominant_gender'])
            race = str(i['dominant_race'])
            emotion = str(i['dominant_emotion'])

            if age >= 60:
                age_text = "Old Adult"
            elif age >= 40:
                age_text = "Middle-aged Adult"
            elif age >= 25:
                age_text = "Young Adult"
            elif age >= 18:
                age_text = "Teen"
            else:
                age_text = "child"

            if silent == False:
                print(f"Age: {str(age)} - {age_text}\nGender: {gender}\nRace: {race}\nEmotion: {emotion}")
            else:    
                #Saving data in csv
                data = [[age, age_text, gender, race, emotion, base_face.rpartition('/')[2]]]
                with open(f'website/static/data/{id}/report.csv','a') as csvfile:
                    np.savetxt(csvfile,data,delimiter=',',fmt='%s', comments='')


        return face_result

    def AllCloneRemover(self, id=False):
        if id:
            path = f"website/static/data/{id}/"
        else:
            path = "./" 
        for x in tqdm (app.ListFiles(id=id), desc="Removing Clones"):
            try:
                x = f"{path}img_final/{x}"
                app.CloneRemover(app.CloneFinder(x,id=id),x,id=id)
            except Exception as e:
                continue

    def FullAnalysis(self, id):  #For website use.
        video = imageio.get_reader(f'website/static/data/{id}/video.mp4')
        for frame_number, im in tqdm (enumerate(video), desc="Extracting Frames"):
            if frame_number % 20 == 0:
                imageio.imwrite(f'website/static/data/{id}/img_src/{frame_number}.jpg', im)


        app.SaveFaces(id)
        #app.AllCloneRemover(id)

        sleep(2)

        for i in tqdm (app.ListFiles(id=id), desc="Analyzing Faces"):
            if i == "representations_facenet.pkl":
                continue
            app.AnalyzeFace(i, silent=True, id=id)



app = AudienceAnalyzer()
if __name__ == '__main__':
    def menu():
        
        print("Welcome to Audience Analyzer!")
        print("Details of the modules in github page.")
        print("1 - Complete Video Analyzer from 0") #video.mp4 for analysis
        print("2 - Save Faces from Frames")
        print("3 - Clone Remover") # Deletes clones in img_final
        print("4 - Analyze Face") # Face Report
        print("5 - Create Report for All")
        menu_c = int(input("Your Selection: "))

        if menu_c == 1:
            app.SplitFrames()
            app.SaveFaces()
            app.AllCloneRemover()

            sleep(2)

            for i in tqdm (app.ListFiles(), desc="Analyzing Faces"):
                if i == "representations_facenet.pkl":
                    continue
                app.AnalyzeFace(i, silent=True)

            print("Done for now.")
        
        if menu_c == 2:
            app.SaveFaces()

        if menu_c == 3:
            app.AllCloneRemover()

        if menu_c == 4:
            app.AnalyzeFace(input("Name of file: "))

        if menu_c == 5:
            for i in tqdm (app.ListFiles(), desc="Analyzing Faces"):
                if i == "representations_facenet.pkl":
                    continue
                app.AnalyzeFace(i, silent=True)
            print("Report Ready.")

        else:
            menu()

    menu()

#app.SplitFrames()
#app.SaveFaces()


#DeepFace.stream(db_path = "./img_src", model_name="Facenet", time_threshold=2)