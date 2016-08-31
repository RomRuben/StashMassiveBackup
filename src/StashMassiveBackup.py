#!/usr/bin/python
import sys
import os
import stashy
import argparse

def connect(url, username, password):
	return stashy.connect(url, username, password)

def createFolder(name):
	if not os.path.exists(name):
		os.makedirs(name)

def changeFolder(name):
	os.chdir(name)

def createAndChangeFolder(projectName):
	createFolder(projectName)
	changeFolder(projectName)

def downloadProject(stash, project):
	projectName = project['name']
	projectList = stash.projects[project['key']].repos.list()
	createAndChangeFolder(projectName)

	print "\n\nProject "+projectName+":\n"

	for repo in projectList:
		for url in repo["links"]["clone"]:
			if (url["name"] == "ssh"):
				os.system("git clone %s" % url["href"])
				break

	print "All repositories in the project has been cloned!"
	changeFolder("../")

def downloadAllProjects(repoName, stash):

	createAndChangeFolder(repoName)

	for project in stash.projects.list():
		downloadProject(stash, project)

	changeFolder("../")


parser = argparse.ArgumentParser(description='MassiveBackup script by romruben')
parser.add_argument('-n', '--name', help = 'Folder name to save the repos', required = True)
parser.add_argument('-l', '--link', help = 'link', required = True)
parser.add_argument('-u', '--user', help = 'user name', required = True)
parser.add_argument('-p', '--password', help = 'user password', required = True)
args = parser.parse_args()

stash = connect(args.link, args.user, args.password)
