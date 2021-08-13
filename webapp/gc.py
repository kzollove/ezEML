import datetime
import glob
import os
import shutil

import click


@click.command()
@click.option('--days', default=30, help='Remove files if JSON last-modified date greater than this number of days')
@click.option('--base', default='/home/pasta/ezeml/user-data', help='Base directory from which to crawl the file system.')
def GC(days, base):
	today = datetime.datetime.today()
	os.chdir(base)

	# get the directories
	for dir in os.listdir(base):
		if os.path.isdir(os.path.join(base, dir)):
			if dir.startswith('.'):
				continue

			# got a user directory
			user_dir = os.path.join(base, dir)

			# remove csv and zip files, if any, left over from earlier versions of ezEML
			try:
				os.chdir(user_dir)
				filelist = list(set(glob.glob(f'{user_dir}/*.csv') + glob.glob(f'{user_dir}/*.zip') +
									glob.glob(f'{user_dir}/*.ezeml')))
				# Iterate over the list of filepaths & remove each file.
				for fpath in filelist:
					try:
						print('Removing', fpath)
						os.remove(fpath)
					except:
						print("Error while deleting file : ", filePath)
			except FileNotFoundError:
				pass

			# find json files that haven't been modified recently
			for file in os.listdir(user_dir):
				if not file.lower().endswith('.json'):
					continue
				filepath = os.path.join(user_dir, file)
				t = os.stat(filepath).st_mtime
				filetime = today - datetime.datetime.fromtimestamp(t)
				if filetime.days > days:

					# have a JSON file modified longer ago than days
					package_name = os.path.splitext(file)[0]

					# remove the uploads dir for this package
					uploads_dir = os.path.join(base, user_dir, 'uploads', package_name)
					if os.path.exists(uploads_dir) and os.path.isdir(uploads_dir):
						try:
							print('Removing uploads', uploads_dir)
							shutil.rmtree(uploads_dir)
						except FileNotFoundError as err:
							print(err)
							pass

					# remove the backups for this JSON file
					backups_dir = os.path.join(user_dir, 'backups')
					try:
						os.chdir(backups_dir)
						filelist = glob.glob(f'{backups_dir}/{file}.*')
						# Iterate over the list of filepaths & remove each file.
						for fpath in filelist:
							if os.path.exists(os.path.join(backups_dir, fpath)):
								try:
									print('Removing', fpath)
									os.remove(fpath)
								except:
									print("Error while deleting file : ", filePath)
					except FileNotFoundError:
						pass

					# remove the exports directory for this package
					exports_dir = os.path.join(user_dir, 'exports', package_name)
					if os.path.exists(exports_dir) and os.path.isdir(exports_dir):
						try:
							print('Removing', exports_dir)
							shutil.rmtree(exports_dir)
						except FileNotFoundError:
							pass


if __name__ == '__main__':
	GC()
