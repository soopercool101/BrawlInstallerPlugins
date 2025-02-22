__author__ = "Squidgy"
__version__ = "1.1.0"

from BrawlInstallerLib import *

def main():
		try: 
			if str(BrawlAPI.RootNode) != "None":
				BrawlAPI.CloseFile()
			if not MainForm.BuildPath:
				BrawlAPI.ShowMessage("Build path must be set. This can be done by navigating to Tools > Settings > General and setting the 'Default Build Path' to the path to your build's root folder.", "Build Path Not Set")
				return
			backupCheck()
			# Get user settings
			if File.Exists(RESOURCE_PATH + '/settings.ini'):
				settings = getSettings()
			else:
				settings = initialSetup()
			# If temporary directory already exists, delete it to prevent duplicate files
			if Directory.Exists(AppPath + '/temp'):
				Directory.Delete(AppPath + '/temp', 1)
			# Prompt the user to pick a zip file
			zipfile = BrawlAPI.OpenFileDialog("Select fighter zip file", "Zip files|*.zip")
			if zipfile:
				# Unzip the file and get temp path
				unzipFile(zipfile)
				folder = AppPath + '/temp'
				if folder:
					# Get all subdirectories in the folder
					fighterDir = Directory.CreateDirectory(folder).GetDirectories()
					# Set up directories
					cspFolder = getDirectoryByName("CSPs", fighterDir)
					cssIconFolder = getDirectoryByName("CSSIcon", fighterDir)
					portraitNameFolder = getDirectoryByName("PortraitName", fighterDir)
					bpFolder = getDirectoryByName("BPs", fighterDir)
					replayIconFolder = getDirectoryByName("ReplayIcon", fighterDir)
					fighterFolder = getDirectoryByName("Fighter", fighterDir)
					exConfigsFolder = getDirectoryByName("EXConfigs", fighterDir)
					moduleFolder = getDirectoryByName("Module", fighterDir)
					soundbankFolder = getDirectoryByName("Soundbank", fighterDir)
					franchiseIconFolder = getDirectoryByName("FranchiseIcons", fighterDir)
					kirbyHatFolder = getDirectoryByName("KirbyHats", fighterDir)
					stockIconFolder = getDirectoryByName("StockIcons", fighterDir)
					victoryThemeFolder = getDirectoryByName("VictoryTheme", fighterDir)
					# Get fighter info
					fighterConfig = Directory.GetFiles(folder + '/EXConfigs', "Fighter*.dat")[0]
					cosmeticConfig = Directory.GetFiles(folder + '/EXConfigs', "Cosmetic*.dat")[0]
					slotConfig = Directory.GetFiles(folder + '/EXConfigs', "Slot*.dat")[0]
					fighterInfo = getFighterInfo(fighterConfig, cosmeticConfig, slotConfig)

					uninstallVictoryTheme = 0
					newSoundbankId = ""
					franchiseIconId = -1
					victoryThemeId = 0
					overwriteFighterName = ""

					#region USER INPUT/PRELIMINARY CHECKS

					# Prompt user to input fighter ID
					idEntered = False
					while idEntered != True:
						fighterId = BrawlAPI.UserStringInput("Enter your desired fighter ID")
						# Ensure fighter ID is just the hex digits
						if fighterId.startswith('0x'):
							fighterId = fighterId.split('0x')[1].upper()
							break
						elif fighterId.isnumeric():
							fighterId = str(hex(int(fighterId))).split('0x')[1].upper()
							break
						else:
							BrawlAPI.ShowMessage("Invalid ID entered!", "Invalid ID")
							continue
					# Check if fighter ID is already used
					existingFighterConfig = getFighterConfig(fighterId)
					if existingFighterConfig:
						overwriteExistingFighter = BrawlAPI.ShowYesNoPrompt("The fighter ID entered is already in use. Do you want to overwrite the existing fighter?", "Overwrite existing fighter?")
						if overwriteExistingFighter == False:
							BrawlAPI.ShowMessage("Fighter installation will abort. Please try again with a different fighter ID.", "Aborting Installation")
							return
					# Check if fighter name is already used
					oldFighterName = ""
					existingFighterName = Directory.GetDirectories(MainForm.BuildPath + '/pf/fighter', fighterInfo.fighterName)
					if existingFighterName:
						overwriteFighterName = BrawlAPI.ShowYesNoPrompt("A fighter with this internal name already exists. Do you want to overwrite it?", "Overwrite fighter name?")
						if overwriteFighterName == False:
							changeFighterName = BrawlAPI.ShowYesNoPrompt("Would you like to change the internal name?", "Change fighter name?")
							if changeFighterName == False:
								BrawlAPI.ShowMessage("Fighter installation will abort.", "Aborting Installation")
								return
							while True and changeFighterName:
								oldFighterName = fighterInfo.fighterName
								fighterInfo.fighterName = BrawlAPI.UserStringInput("Enter your desired fighter name")
								existingFighterName = Directory.GetDirectories(MainForm.BuildPath + '/pf/fighter', fighterInfo.fighterName)
								if existingFighterName:
									repeatFighterName = BrawlAPI.ShowYesNoPrompt("Fighter name already in use! Try a different name?", "Try again?")
									if repeatFighterName:
										continue
									else:
										BrawlAPI.ShowMessage("Fighter installation will abort.", "Aborting Installation")
										return
								else:
									break
					# Prompt user to input cosmetic ID
					idEntered = False
					while idEntered != True:
						cosmeticId = BrawlAPI.UserStringInput("Enter your desired cosmetic ID")
						# Ensure cosmetic ID is the integer format
						if cosmeticId.startswith('0x'):
							cosmeticId = int(cosmeticId, 16)
							break
						elif cosmeticId.isnumeric():
							cosmeticId = int(cosmeticId)
							break
						else:
							BrawlAPI.ShowMessage("Invalid ID entered!", "Invalid ID")
							continue
					# Check if cosmetic ID is already used
					existingFile = Directory.GetFiles(MainForm.BuildPath + '/pf/menu/common/char_bust_tex', "MenSelchrFaceB" + addLeadingZeros(cosmeticId, 2) + "0.brres")
					if existingFile:
						overwriteExistingCosmetic = BrawlAPI.ShowYesNoPrompt("The cosmetic ID entered is already in use. Do you want to overwrite the existing cosmetics?", "Overwrite existing cosmetics?")
						if overwriteExistingCosmetic == False:
							BrawlAPI.ShowMessage("Fighter installation will abort. Please try again with a different cosmetic ID.", "Aborting Installation")
							return
					# Victory theme checks
					if victoryThemeFolder:
						# Ask user if they would like to install the included victory theme
						installVictoryTheme = BrawlAPI.ShowYesNoPrompt("This fighter comes with a victory theme. Would you like to install it?", "Install victory theme?")
						if installVictoryTheme == False:
							changeVictoryTheme = BrawlAPI.ShowYesNoPrompt("Would you like to change this fighter's victory theme ID?", "Change victory theme?")
							while changeVictoryTheme:
								victoryThemeId = BrawlAPI.UserStringInput("Enter your desired victory theme ID")
								# Ensure victory theme ID is in integer format
								if victoryThemeId.startswith('0x'):
									victoryThemeId = int(victoryThemeId, 16)
									break
								elif victoryThemeId.isnumeric():
									victoryThemeId = int(victoryThemeId)
									break
								else:
									BrawlAPI.ShowMessage("Invalid ID entered!", "Invalid ID")
									continue
						# Check if existing fighter has a different victory theme
						if installVictoryTheme:
							existingSlotConfig = getSlotConfig(fighterId)
							if existingSlotConfig:
								oldVictoryThemeName = getVictoryThemeByFighterId(fighterId)
								if oldVictoryThemeName:
									victoryThemeName = FileInfo(Directory.GetFiles(folder + '/VictoryTheme', "*.brstm")[0]).Name
									if oldVictoryThemeName != victoryThemeName.split('.brstm')[0]:
										uninstallVictoryTheme = BrawlAPI.ShowYesNoPrompt("Previously installed fighter contains a victory theme with a different name. Do you want to remove it?", "Remove existing victory theme?")
						
					# Check if soundbank is already in use
					if soundbankFolder:
						soundbankId = str(hex(int(fighterInfo.soundbankId))).split('0x')[1].upper()
						# Get soundbank name to check
						modifier = 0 if settings.addSevenToSoundbankName == "false" else 7
						if settings.soundbankStyle == "hex":
							soundbankNameToCheck = str(hex(int(soundbankId, 16) + modifier)).split('0x')[1].upper()
						else:
							soundbankNameToCheck = str(int(soundbankId, 16) + modifier)
						soundbankMatch = Directory.GetFiles(MainForm.BuildPath + '/pf/sfx', soundbankNameToCheck + '.sawnd')
						if soundbankMatch and settings.sfxChangeExe != "" and settings.sawndReplaceExe != "":
							changeSoundbankId = BrawlAPI.ShowYesNoPrompt("A soundbank with the same ID already exists. Would you like to change the soundbank ID?", "Soundbank Already Exists")
							if changeSoundbankId:
								matchFound = True
								# Keep prompting for alternate soundbank ID until one that is not used is entered
								while matchFound:
									newSoundbankId = BrawlAPI.UserStringInput("Enter your desired soundbank ID")
									# Ensure soundbank ID is just the hex digits
									if newSoundbankId.startswith('0x'):
										newSoundbankId = newSoundbankId.split('0x')[1]
									elif newSoundbankId.isnumeric():
										newSoundbankId = str(hex(int(newSoundbankId))).split('0x')[1].upper()
									else:
										BrawlAPI.ShowMessage("Invalid ID entered!", "Invalid ID")
										continue
									if settings.soundbankStyle == "hex":
										soundbankNameToCheck = str(hex(int(newSoundbankId, 16) + modifier)).split('0x')[1].upper()
									else:
										soundbankNameToCheck = str(int(newSoundbankId, 16) + modifier)
									soundbankMatch = Directory.GetFiles(MainForm.BuildPath + '/pf/sfx', newSoundbankId + '.sawnd')
									if soundbankMatch:
										tryAgain = BrawlAPI.ShowYesNoPrompt("Soundbank ID entered already exists. Try entering a different ID?", "Soundbank Already Exists")
										if tryAgain == False:
											BrawlAPI.ShowMessage("Fighter installation will abort.", "Aborting Installation")
											return
										continue
									matchFound = False
							else:
								newSoundbankId = ""
						elif soundbankMatch:
							overwriteSoundbank = BrawlAPI.ShowYesNoPrompt("A soundbank with the same ID already exists. You do not have soundbank ID changing set up. Would you like to overwrite the current soundbank?", "Soundbank Already Exists")
							if overwriteSoundbank == False:
								BrawlAPI.ShowMessage("Fighter installation will abort.", "Aborting Installation")
								return
					# Franchise icon install prompt
					if franchiseIconFolder:
						doInstallFranchiseIcon = BrawlAPI.ShowYesNoPrompt("This character comes with a franchise icon. Would you like to install it?", "Install Franchise Icon")
						if doInstallFranchiseIcon:
							franchiseIconUsed = True
							while franchiseIconUsed:
								franchiseIconId = BrawlAPI.UserStringInput("Enter your desired franchise icon ID")
								# Ensure franchise icon ID is in integer format
								if franchiseIconId.startswith('0x'):
									franchiseIconId = int(franchiseIconId, 16)
								elif franchiseIconId.isnumeric():
									franchiseIconId = int(franchiseIconId)
								else:
									BrawlAPI.ShowMessage("Invalid ID entered!", "Invalid ID")
									continue
								franchiseIconUsed = franchiseIconIdUsed(franchiseIconId)
								if franchiseIconUsed:
									changeFranchiseIconId = BrawlAPI.ShowYesNoPrompt("A franchise icon with this ID already exists. Would you like to enter a different ID?", "Franchise Icon Already Exists")
									if changeFranchiseIconId == False:
										BrawlAPI.ShowMessage("Fighter installation will abort.", "Aborting Installation")
										BrawlAPI.ForceCloseFile()
										return
									continue
								else:
									BrawlAPI.ForceCloseFile()
									break
						else:
							newFranchiseIconId = BrawlAPI.ShowYesNoPrompt("Would you like to change the franchise icon ID for this fighter?", "Change franchise icon ID?")
							while newFranchiseIconId:
								franchiseIconId = BrawlAPI.UserStringInput("Enter your desired franchise icon ID")
								# Ensure franchise icon ID is in integer format
								if franchiseIconId.startswith('0x'):
									franchiseIconId = int(franchiseIconId, 16)
									break
								elif franchiseIconId.isnumeric():
									franchiseIconId = int(franchiseIconId)
									break
								else:
									BrawlAPI.ShowMessage("Invalid ID entered!", "Invalid ID")
									continue
					#endregion USER INPUT/PRELIMINARY CHECKS

					# Set up progressbar
					progressCounter = 0
					progressBar = ProgressWindow(MainForm.Instance, "Installing Character...", "Installing Character", False)
					progressBar.Begin(0, 14, progressCounter)

					#region SCSELCHARACTER

					# Install CSPs
					if cspFolder:
						installCSPs(cosmeticId, cspFolder, settings.rspLoading)
					# Install CSS icon
					if cssIconFolder:
						# Get user's preferred icon style
						iconFolders = Directory.GetDirectories(cssIconFolder.FullName, settings.cssIconStyle)
						if iconFolders:
							# Use CMPR for Brawl/PM style icons
							if settings.cssIconStyle == "vBrawl" or settings.cssIconStyle == "PM":
								format = WiiPixelFormat.CMPR
							else:
								format = WiiPixelFormat.CI8
							installCSSIcon(cosmeticId, Directory.GetFiles(iconFolders[0], "*.png")[0], format)
							nameFolders = Directory.GetDirectories(iconFolders[0], "Name")
							# If a name folder is found in the CSS icon directory, install CSS icon name
							if nameFolders:
								installCSSIconName(cosmeticId, Directory.GetFiles(nameFolders[0], "*.png")[0])
						else:
							BrawlAPI.ShowMessage("Could not find CSS icon in a format that matches your preferences. CSS icon installation will be skipped. Please install a CSS icon manually.", "CSS Icon Not Found")
					# Install CSS portrait name
					if portraitNameFolder and settings.installPortraitNames == "true":
						nameFolders = Directory.GetDirectories(portraitNameFolder.FullName, settings.portraitNameStyle)
						if nameFolders:
							installPortraitName(cosmeticId, Directory.GetFiles(nameFolders[0], "*.png")[0])
						else:
							BrawlAPI.ShowMessage("Could not find portrait name in a format that matches your preferences. Portrait name installation will be skipped. Please install a portrait name manually.", "Portrait Name Not Found")
					# Install stock icons to sc_selcharacter
					if stockIconFolder and settings.installStocksToCSS == "true":
						installStockIcons(cosmeticId, stockIconFolder, "Misc Data [90]", "", rootName="", filePath='/pf/menu2/sc_selcharacter.pac', fiftyCC=settings.fiftyCostumeCode)
					# Install franchise icon to sc_selcharacter
					if franchiseIconFolder and doInstallFranchiseIcon:
						franchiseIconFolderCss = Directory.GetDirectories(franchiseIconFolder.FullName, "Black")
						installFranchiseIcon(franchiseIconId, Directory.GetFiles(franchiseIconFolderCss[0], "*.png")[0], '/pf/menu2/sc_selcharacter.pac', int(settings.franchiseIconSizeCSS))
					# If we did any work in sc_selcharacter, save and close it
					fileOpened = checkOpenFile("sc_selcharacter")
					if fileOpened:
						BrawlAPI.SaveFile()
						BrawlAPI.ForceCloseFile()

					progressCounter += 1
					progressBar.Update(progressCounter)

					#endregion SCSELCHARACTER

					#region info.pac

					# Install stock icons to info.pac
					if stockIconFolder and settings.installStocksToInfo == "true":
						installStockIcons(cosmeticId, stockIconFolder, "Misc Data [30]", "Misc Data [30]", rootName="", filePath='/pf/info2/info.pac', fiftyCC=settings.fiftyCostumeCode)
					# Install franchise icon to info.pac
					if franchiseIconFolder and doInstallFranchiseIcon:
						franchisIconFolderInfo = Directory.GetDirectories(franchiseIconFolder.FullName, "Black")
						installFranchiseIcon(franchiseIconId, Directory.GetFiles(franchisIconFolderInfo[0], "*.png")[0], '/pf/info2/info.pac')
					fileOpened = checkOpenFile("info")
					if fileOpened:
						BrawlAPI.SaveFile()
						BrawlAPI.ForceCloseFile()

					progressCounter += 1
					progressBar.Update(progressCounter)
					
					#endregion info.pac

					#region STGRESULT

					# Install stock icons to STGRESULT
					if stockIconFolder and settings.installStockIconsToResult == "true":
						installStockIcons(cosmeticId, stockIconFolder, "Misc Data [120]", "Misc Data [110]", rootName="2", filePath='/pf/stage/melee/STGRESULT.pac', fiftyCC=settings.fiftyCostumeCode)
					# Install franchise icon to STGRESULT
					if franchiseIconFolder and doInstallFranchiseIcon:
						franchisIconFolderResult = Directory.GetDirectories(franchiseIconFolder.FullName, "Transparent")
						installFranchiseIconResult(franchiseIconId, Directory.GetFiles(franchisIconFolderResult[0], "*.png")[0])
					fileOpened = checkOpenFile("STGRESULT")
					if fileOpened:
						BrawlAPI.SaveFile()
						BrawlAPI.ForceCloseFile()

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion STGRESULT

					#region Other Stock Icon Locations

					if stockIconFolder:
						# StockFaceTex.brres - used for things like rotation mode
						if settings.installStocksToStockFaceTex == "true":
							installStockIcons(cosmeticId, stockIconFolder, "", "", filePath='/pf/menu/common/StockFaceTex.brres', fiftyCC=settings.fiftyCostumeCode)
							BrawlAPI.SaveFile()
							BrawlAPI.ForceCloseFile()
						# sc_selmap - used for SSS in vBrawl
						if settings.installStocksToSSS == "true":
							installStockIcons(cosmeticId, stockIconFolder, "Misc Data [40]", "Misc Data [20]", filePath='/pf/menu2/sc_selmap.pac', fiftyCC=settings.fiftyCostumeCode)
							BrawlAPI.SaveFile()
							BrawlAPI.ForceCloseFile()

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion Other Stock Icon Locations

					#region BPs

					if bpFolder:
						# Get user's preferred BP style
						bpFolders = Directory.GetDirectories(bpFolder.FullName, settings.bpStyle)
						if bpFolders:
							installBPs(cosmeticId, Directory.GetFiles(bpFolders[0], "*.png"), fiftyCC=settings.fiftyCostumeCode)
						else:
							bpFolders = Directory.GetDirectories(bpFolder.FullName, "vBrawl")
							if bpFolders:
								installBPs(cosmeticId, Directory.GetFiles(bpFolders[0], "*.png"), fiftyCC=settings.fiftyCostumeCode)

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion BPs

					#region Replay Icon

					if replayIconFolder:
						installReplayIcon(cosmeticId, Directory.GetFiles(replayIconFolder.FullName, "*.png")[0])
					progressCounter += 1
					progressBar.Update(progressCounter)

					#endregion Replay Icon

					#region Victory Theme

					# If user indicated they want victory theme removed, remove it first
					if uninstallVictoryTheme:
						removeSongId = getVictoryThemeIDByFighterId(fighterId)
						removeVictoryTheme(removeSongId)
					# Add victory theme
					if victoryThemeFolder and settings.installVictoryThemes == "true" and installVictoryTheme:
						victoryThemeId = addVictoryTheme(Directory.GetFiles(victoryThemeFolder.FullName, "*.brstm")[0])

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion Victory Theme

					#region Soundbank

					# Update soundbank ID if user set to do that
					if newSoundbankId:
						updateSoundbankId(FileInfo(Directory.GetFiles(fighterFolder.FullName, "Fit" + fighterInfo.fighterName + ".pac")[0]), FileInfo(settings.sawndReplaceExe), FileInfo(settings.sfxChangeExe), str("%x" % fighterInfo.soundbankId).upper(), newSoundbankId, settings.addSevenToSoundbankIds)

					# Move soundbank
					if soundbankFolder:
						# Rename file based on user preferences
						if newSoundbankId == "":
							newSoundbankId = "%x" % fighterInfo.soundbankId
						modifier = 0 if settings.addSevenToSoundbankName == "false" else 7
						if settings.soundbankStyle == "hex":
							newSoundbankId = str(hex(int(newSoundbankId, 16) + modifier)).split('0x')[1].upper()
						else:
							newSoundbankId = str(int(newSoundbankId, 16) + modifier)
						moveSoundbank(FileInfo(Directory.GetFiles(soundbankFolder.FullName, "*.sawnd")[0]), newSoundbankId)

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion Soundbank

					#region Kirby Hats

					kirbyHatFighterId = -1
					if settings.kirbyHatExe != "":
						if kirbyHatFolder:
							# Attempt to get the kirby hat fighter ID from text file
							fighterIdFile = getFileByName("FighterID.txt", kirbyHatFolder)
							if fighterIdFile:
								fighterIdString = File.ReadAllText(fighterIdFile.FullName)
								# Ensure fighter ID is the integer format
								if fighterIdString.startswith('0x'):
									kirbyHatFighterId = int(fighterIdString, 16)
								elif fighterIdString.isnumeric():
									kirbyHatFighterId = int(fighterIdString)
						# If we don't have a kirby hat fighter ID but settings say we should, generate kirby hat based on settings
						if kirbyHatFighterId == -1 and settings.defaultKirbyHat != "none":
							# Delete Kirby hat folder if it already exists
							if kirbyHatFolder:
								Directory.Delete(kirbyHatFolder.FullName, 1)
							# Create the kirby hat folder
							kirbyHatFolder = Directory.CreateDirectory(AppPath + '/temp/KirbyHats')
							# Get name of fighter based on default kirby hat ID
							kirbyHatFighterId = int(settings.defaultKirbyHat, 16)
							kirbyHatFighterName = FIGHTER_IDS[kirbyHatFighterId]
							# Get Kirby hat files from the build and copy them to the temp directory
							kirbyHatFiles = Directory.GetFiles(MainForm.BuildPath + '/pf/fighter/kirby', "FitKirby" + kirbyHatFighterName + "*.pac")
							# Rename them appropriately
							for kirbyHatFile in kirbyHatFiles:
								# Back up Kirby hat files if they already exist
								createBackup(FileInfo(kirbyHatFile).FullName.replace(kirbyHatFighterName, fighterInfo.fighterName))
								File.Copy(kirbyHatFile, AppPath + '/temp/KirbyHats/' + FileInfo(kirbyHatFile).Name.replace(kirbyHatFighterName, fighterInfo.fighterName), 1)
						# Install Kirby hat
						if settings.defaultKirbyHat != "none":
							if existingFighterName and overwriteFighterName:
								# If we are overwriting an existing fighter name, clean up the old Kirby hats
								deleteKirbyHatFiles(DirectoryInfo(existingFighterName[0]).Name)
							installKirbyHat(fighterInfo.characterName, fighterInfo.fighterName, fighterId, str("%x" % kirbyHatFighterId).upper(), settings.kirbyHatExe, Directory.GetFiles(kirbyHatFolder.FullName, "FitKirby*.pac"), oldFighterName, fighterInfo.fighterName)

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion Kirby Hats

					#region Fighter Files

					# Install fighter files
					existingFighterConfigName = ""
					if fighterFolder:
						if overwriteFighterName and existingFighterName:
							deleteFighterFiles(DirectoryInfo(existingFighterName[0]).Name.lower())
						# If a fighter already exists at this ID, delete them
						if existingFighterConfig:
							BrawlAPI.OpenFile(existingFighterConfig)
							existingFighterConfigName = BrawlAPI.RootNode.FighterName
							BrawlAPI.ForceCloseFile()
						installFighterFiles(Directory.GetFiles(fighterFolder.FullName, "*.pac"), fighterInfo.fighterName, existingFighterConfigName, oldFighterName)

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion Fighter Files

					#region Module

					# Update and install module file
					if moduleFolder:
						installModuleFile(Directory.GetFiles(moduleFolder.FullName, "*.rel")[0], moduleFolder, fighterId, fighterInfo.fighterName, existingFighterConfigName)

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion Module

					#region EX Configs

					# Update and move EX configs
					if exConfigsFolder:
						useKirbyHat = False if settings.defaultKirbyHat == "none" or kirbyHatFighterId == -1 else True
						modifyExConfigs(Directory.GetFiles(exConfigsFolder.FullName, "*.dat"), cosmeticId, fighterId, fighterInfo.fighterName, franchiseIconId, useKirbyHat, newSoundbankId, victoryThemeId, kirbyHatFighterId)

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion EX Configs

					#region Code Menu

					# Add fighter to code menu
					if settings.assemblyFunctionsExe != "":
						addToCodeMenu(fighterInfo.characterName, fighterId, settings.assemblyFunctionsExe)

					progressCounter += 1
					progressBar.Update(progressCounter)
					#endregion Code Menu

					#region CSSRoster

					# Add fighter to roster
					if settings.useCssRoster == "true":
						changesMade = addToRoster(fighterId)
						if changesMade:
							BrawlAPI.SaveFile()
						BrawlAPI.ForceCloseFile()

					progressBar.Finish()
					#endregion
					
				# Delete temporary directory
				Directory.Delete(AppPath + '/temp', 1)
				archiveBackup()
				BrawlAPI.ShowMessage("Character successfully installed.", "Success")
		except Exception as e:
			BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
			BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
			restoreBackup()
			archiveBackup()



main()