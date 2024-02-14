# ref: https://github.com/acheong08/BingImageCreator/blob/main/README.md
'''
HOW-TO get required coockie
login to bing.com/image/creator
  open inspector (F12)
  generate an image on the webpage
  then go back to the opened inspector 
   then go to 'network' tab
   then use console cmd: cookieStore.get("_U")
   then search output for 'value' and copy it (thats the cookie)
'''

# LOGGED EXCEPTIONS...
'''
 raise Exception("Bad images")
Exception: Bad images

 raise Exception(error_redirect)
Exception: Redirect failed
'''
import os
import webbrowser
cook = "1CIx4heldQFrBstIQ-KL7d7ix-Rif8Di0yW_vsuk-Gsfb9lGzgTWTQ20KJ5oJR_Y7bmVNNKrKS_MVEN4v-OjGPVVsQ2a-h9zZkMC90Fj74frtXRSfKPzzJ5p8hdX27bfvEgUQlVJAzC92Mo_dFLTYvr_SgpQrFp-eUbdI-cByE9F57vWbER9z287be7cdsw6TP1_BYzzC9G1jkpYMgi-vYw"
os.environ["BING_COOKIES"] = cook

# import os
# import shutil

# from src.BingImageCreator import ImageGen
from BingImageCreator import ImageGen

def test_gen_image():
    # create a temporary output directory for testing purposes
    test_output_dir = "test_output"
    # os.mkdir(test_output_dir)
    # download a test image
    test_image_url = "https://picsum.photos/200"
    # gen = ImageGen(auth_cookie="")
    gen = ImageGen(auth_cookie=cook, auth_cookie_SRCHHPGUSR=cook)
    str_prompt = input("\n describe the image ...\n > ")
    # str_prompt = "a bear saying hello"
    lst_imgs = gen.get_images(str_prompt)
    print('DONE GETTING IMAGES...')
    print(*lst_imgs, sep='\n')
    print('LAUNCHING IMAGES...')

    for url in lst_imgs:
        safari = webbrowser.get('safari')  # specify the browser
        safari.open_new_tab(url)

    

test_gen_image()

def test_save_images():
    # create a temporary output directory for testing purposes
    test_output_dir = "test_output"
    os.mkdir(test_output_dir)
    # download a test image
    test_image_url = "https://picsum.photos/200"
    # gen = ImageGen(auth_cookie="")
    gen = ImageGen(auth_cookie=cook)
    str_prompt = "a bear saying hello"
    lst_imgs = gen.get_images(str_prompt)
    print(lst_imgs)
    
    # gen.save_images([test_image_url], test_output_dir)
    # gen.save_images([test_image_url], test_output_dir, file_name="test_image")
    # # check if the image was downloaded and saved correctly
    # assert os.path.exists(os.path.join(test_output_dir, "test_image_0.jpeg"))
    # assert os.path.exists(os.path.join(test_output_dir, "0.jpeg"))
    # # remove the temporary output directory
    # shutil.rmtree(test_output_dir)

# from openai import OpenAI
# client = OpenAI(api_key="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")
# # BearShares key: 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

# response = client.images.generate(
#   model="dall-e-3",
#   prompt="a white siamese cat",
#   size="1024x1024",
#   quality="standard",
#   n=1,
# )

# image_url = response.data[0].url