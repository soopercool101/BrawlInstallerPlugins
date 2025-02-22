__author__ = "Squidgy"
__version__ = "1.0.1"

from BrawlInstallerLib import *

def main():
		# If temporary directory already exists, delete it to prevent duplicate files
		if Directory.Exists(AppPath + '/temp'):
			Directory.Delete(AppPath + '/temp', 1)

		title = "Character Packaging Tool"
		# EX Configs
		exConfigs = BrawlAPI.OpenMultiFileDialog("Select fighter EX config files", "DAT files|*.dat")
		# Fighter files
		fighterFiles = BrawlAPI.OpenMultiFileDialog("Select fighter pac files", "PAC files|*.pac")
		# Module file
		moduleFile = BrawlAPI.OpenFileDialog("Select fighter module file", "REL files|*.rel")
		BrawlAPI.ShowMessage("You will be prompted to select your fighter's CSP files. When you select multiple files, they will be color smashed.\n\nYou will receive the prompt multiple times, so you can have multiple sets of CSPs that are not all color smashed together.", title)
		# CSPs
		cspFiles = []
		while True:
			cspsToAdd = BrawlAPI.OpenMultiFileDialog("Select fighter CSP files (if multiple, images will be color smashed)", "PNG files|*.png")
			if cspsToAdd:
				cspFiles.append(cspsToAdd)
			continueCSP = BrawlAPI.ShowYesNoPrompt("Do you have additional costumes to import?", title)
			if continueCSP:
				continue
			else:
				break
		# BPs
		bpFiles = BrawlAPI.OpenMultiFileDialog("Select vBrawl BP files", "PNG files|*.png")
		remixBpFiles = BrawlAPI.OpenMultiFileDialog("Select REMIX BP files", "PNG files|*.png")

		# CSS Icons
		pPlusIcon = BrawlAPI.OpenFileDialog("Select P+ style CSS icon", "PNG files|*.png")

		pmIcon = BrawlAPI.OpenFileDialog("Select PM style CSS icon", "PNG files|*.png")
		pmIconName = BrawlAPI.OpenFileDialog("Select PM style CSS icon nameplate", "PNG files|*.png")

		remixIcon = BrawlAPI.OpenFileDialog("Select REMIX style CSS icon", "PNG files|*.png")

		brawlIcon = BrawlAPI.OpenFileDialog("Select vBrawl style CSS icon", "PNG files|*.png")
		brawlIconName = BrawlAPI.OpenFileDialog("Select vBrawl style CSS icon nameplate", "PNG files|*.png")

		# Portrait Names
		pmName = BrawlAPI.OpenFileDialog("Select PM style portrait name", "PNG files|*.png")
		
		brawlName = BrawlAPI.OpenFileDialog("Select vBrawl style portrait name", "PNG files|*.png")

		# Stocks
		BrawlAPI.ShowMessage("You will be prompted to select your fighter's stock icon files. When you select multiple files, they will be color smashed.\n\nYou will receive the prompt multiple times, so you can have multiple sets of stocks that are not all color smashed together.", title)
		stockIcons = []
		while True:
			stockIconsToAdd = BrawlAPI.OpenMultiFileDialog("Select fighter stock icon files (if multiple, images will be color smashed)", "PNG files|*.png")
			if stockIconsToAdd:
				stockIcons.append(stockIconsToAdd)
			continueStockIcons = BrawlAPI.ShowYesNoPrompt("Do you have additional costumes to import?", title)
			if continueStockIcons:
				continue
			else:
				break

		# Replay Icon
		replayIcon = BrawlAPI.OpenFileDialog("Select replay icon", "PNG files|*.png")

		# Soundbank
		soundbank = BrawlAPI.OpenFileDialog("Select soundbank file", "SAWND files|*.sawnd")

		# Kirby hats
		installKirbyHats = BrawlAPI.ShowYesNoPrompt("Does your fighter have Kirby hat files to import?", title)
		if installKirbyHats:
			kirbyHatFiles = BrawlAPI.OpenMultiFileDialog("Select your fighter's kirby hat PAC files", "PAC files|*.pac")
			# Prompt user to input kirby hat fighter ID
			idEntered = False
			while idEntered != True:
				kirbyHatId = BrawlAPI.UserStringInput("Enter the fighter ID for your kirby hat")
				# Ensure fighter ID is just the hex digits
				if kirbyHatId.startswith('0x'):
					kirbyHatId = kirbyHatId
					break
				elif kirbyHatId.isnumeric():
					kirbyHatId = '0x' + str(hex(int(kirbyHatId))).split('0x')[1].upper()
					break
				else:
					BrawlAPI.ShowMessage("Invalid ID entered!", "Invalid ID")
					continue
		else:
			kirbyHatFiles = 0
			kirbyHatId = ''

		# Franchise Icons
		franchiseIconBlack = BrawlAPI.OpenFileDialog("Select franchise icon with black background", "PNG files|*.png")
		franchiseIconTransparent = BrawlAPI.OpenFileDialog("Select franchise icon with transparent background", "PNG files|*.png")

		# Victory Theme
		victoryTheme = BrawlAPI.OpenFileDialog("Select your victory .brstm file", "BRSTM files|*.brstm")

		# Stage directory
		Directory.CreateDirectory(AppPath + '/temp')

		if exConfigs:
			for file in exConfigs:
				copyFile(file, AppPath + '/temp/EXConfigs')

		if fighterFiles:
			for file in fighterFiles:
				copyFile(file, AppPath + '/temp/Fighter')

		if moduleFile:
			copyFile(moduleFile, AppPath + '/temp/Module')
		if cspFiles != []:
			i = 1
			for fileSet in cspFiles:
				j = 1
				for file in fileSet:
					copyRenameFile(file, addLeadingZeros(str(j), 4) + '.png', AppPath + '/temp/CSPs/' + addLeadingZeros(str(i), 4))
					j += 1
				i += 1

		if bpFiles:
			i = 1
			for file in bpFiles:
				copyRenameFile(file, addLeadingZeros(str(i), 4) + '.png', AppPath + '/temp/BPs/vBrawl')
				i += 1

		if remixBpFiles:
			i = 1
			for file in remixBpFiles:
				copyRenameFile(file, addLeadingZeros(str(i), 4) + '.png', AppPath + '/temp/BPs/REMIX')
				i += 1

		if pPlusIcon:
			copyFile(pPlusIcon, AppPath + '/temp/CSSIcon/P+')

		if pmIcon:
			copyFile(pmIcon, AppPath + '/temp/CSSIcon/PM')
			if pmIconName:
				copyFile(pmIconName, AppPath + '/temp/CSSIcon/PM/Name')

		if remixIcon:
			copyFile(remixIcon, AppPath + '/temp/CSSIcon/REMIX')

		if brawlIcon:
			copyFile(brawlIcon, AppPath + '/temp/CSSIcon/vBrawl')
			if brawlIconName:
				copyFile(brawlIconName, AppPath + '/temp/CSSIcon/vBrawl/Name')

		if pmName:
			copyFile(pmName, AppPath + '/temp/PortraitName/PM')

		if brawlName:
			copyFile(brawlName, AppPath + '/temp/PortraitName/vBrawl')

		if replayIcon:
			copyFile(replayIcon, AppPath + '/temp/ReplayIcon')

		if stockIcons != []:
			i = 1
			for fileSet in stockIcons:
				j = 1
				for file in fileSet:
					copyRenameFile(file, addLeadingZeros(str(j), 4) + '.png', AppPath + '/temp/StockIcons/' + addLeadingZeros(str(i), 4))
					j += 1
				i += 1

		if soundbank:
			copyFile(soundbank, AppPath + '/temp/Soundbank')

		if kirbyHatFiles:
			for file in kirbyHatFiles:
				copyFile(file, AppPath + '/temp/KirbyHats')
			if kirbyHatId:
				File.WriteAllText(AppPath + '/temp/KirbyHats/FighterID.txt', kirbyHatId)

		if franchiseIconBlack:
			copyFile(franchiseIconBlack, AppPath + '/temp/FranchiseIcons/Black')
		
		if franchiseIconTransparent:
			copyFile(franchiseIconTransparent, AppPath + '/temp/FranchiseIcons/Transparent')

		if victoryTheme:
			copyFile(victoryTheme, AppPath + '/temp/VictoryTheme')

		outputDirectory = BrawlAPI.OpenFolderDialog("Select output directory")
		fileName = BrawlAPI.UserStringInput("Enter a file name")

		args = 'a -y -bsp0 -bso0 -bd "' + outputDirectory + '/' + fileName + '.zip" "' + AppPath + '/temp/*"'
		p = Process.Start(RESOURCE_PATH + '/7za.exe', args)
		p.WaitForExit()
		p.Dispose()

		BrawlAPI.ShowMessage("Fighter package created at " + outputDirectory + '\\' + fileName + '.zip', title)

main()