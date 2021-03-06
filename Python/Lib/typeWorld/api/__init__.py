# -*- coding: utf-8 -*-

from typeWorld.api.base import *
import functools


WEBRESOURCEDESCRIPTION = '\n\nIf you want to make sure that the app loads the latest version of this resource, consider making the URL unique. You could enforce it by adding a unique string to it, such as the time the resource was added to your server, e.g. http://awesomefonts.com/images/logo.svgz?timeadded=1516886401'

####################################################################################################################################

#  LicenseDefinition

class LicenseDefinition(DictBasedObject):
	# 	key: 					[data type, required, default value, description]
	_structure = {
		'keyword':	 				[UnicodeDataType,		True, 	None, 	'Machine-readable keyword under which the license will be referenced from the individual fonts.'],
		'name':	 					[MultiLanguageTextProxy,		True, 	None, 	'Human-readable name of font license'],
		'URL':	 					[WebURLDataType,		True, 	None, 	'URL where the font license text can be viewed online'],
	}

	def __repr__(self):
		return '<LicenseDefinition "%s">' % self.name or self.keyword or 'undefined'

def LicenseDefinition_Parent(self):
	if hasattr(self, '_parent') and hasattr(self._parent, '_parent') and hasattr(self._parent._parent, '_parent'):
		return self._parent._parent._parent
LicenseDefinition.parent = property(lambda self: LicenseDefinition_Parent(self))

class LicenseDefinitionProxy(Proxy):
	dataType = LicenseDefinition

class LicenseDefinitionListProxy(ListProxy):
	dataType = LicenseDefinitionProxy



####################################################################################################################################

#  LicenseUsage

class LicenseUsage(DictBasedObject):
	# 	key: 					[data type, required, default value, description]
	_structure = {

		'keyword':						[UnicodeDataType,		True, 	None, 	'Keyword reference of font’s license. This license must be specified in ::Foundry.licenses::'],
		'seatsAllowedForUser':			[IntegerDataType,		False, 	None, 	'In case of desktop font (see ::Font.purpose::), number of installations permitted by the user’s license.'],
		'seatsInstalledByUser':			[IntegerDataType,		False, 	None, 	'In case of desktop font (see ::Font.purpose::), number of installations recorded by the API endpoint. This value will need to be supplied dynamically by the API endpoint through tracking all font installations through the "anonymousAppID" parameter of the "%s" and "%s" command. Please note that the Type.World client app is currently not designed to reject installations of the fonts when the limits are exceeded. Instead it is in the responsibility of the API endpoint to reject font installations though the "%s" command when the limits are exceeded. In that case the user will be presented with one or more license upgrade links.' % (INSTALLFONTCOMMAND['keyword'], UNINSTALLFONTCOMMAND['keyword'], INSTALLFONTCOMMAND['keyword'])],
		'allowanceDescription':			[MultiLanguageTextProxy,False, 	None, 	'In case of non-desktop font (see ::Font.purpose::), custom string for web fonts or app fonts reminding the user of the license’s limits, e.g. "100.000 page views/month"'],
		'upgradeURL':					[WebURLDataType,		False, 	None, 	'URL the user can be sent to to upgrade the license of the font, for instance at the foundry’s online shop. If possible, this link should be user-specific and guide him/her as far into the upgrade process as possible.'],
		'dateAddedForUser':				[DateDataType,			False, 	None, 	'Date that the user has purchased this font or the font has become available to the user otherwise (like a new font within a foundry’s beta font repository). Will be used in the UI to signal which fonts have become newly available in addition to previously available fonts. This is not to be confused with the ::Version.releaseDate::, although they could be identical.'],

		# 'keyword':	 				[UnicodeDataType,		True, 	None, 	'Machine-readable keyword under which the license will be referenced from the individual fonts.'],
		# 'name':	 					[MultiLanguageTextProxy,		True, 	None, 	'Human-readable name of font license'],
		# 'URL':	 					[WebURLDataType,		True, 	None, 	'URL where the font license text can be viewed online'],
	}

	def __repr__(self):
		return '<LicenseUsage "%s">' % self.keyword or 'undefined'

	def customValidation(self):
		information, warnings, critical = [], [], []

		# Checking for existing license
		if not self.getLicense():
			critical.append('%s has license "%s", but %s has no matching license.' % (self, self.keyword, self.parent.parent.parent))

		return information, warnings, critical

	def getLicense(self):
		'''\
		Returns the ::License:: object that this font references.
		'''
		return self.parent.parent.parent.getLicenseByKeyword(self.keyword)

def LicenseUsage_Parent(self):
	if hasattr(self, '_parent') and hasattr(self._parent, '_parent') and hasattr(self._parent._parent, '_parent'):
		return self._parent._parent._parent
LicenseUsage.parent = property(lambda self: LicenseUsage_Parent(self))

class LicenseUsageProxy(Proxy):
	dataType = LicenseUsage

class LicenseUsageListProxy(ListProxy):
	dataType = LicenseUsageProxy



####################################################################################################################################

#  Designer

class Designer(DictBasedObject):
	# 	key: 					[data type, required, default value, description]
	_structure = {
		'keyword':	 				[UnicodeDataType,		True, 	None, 	'Machine-readable keyword under which the designer will be referenced from the individual fonts or font families'],
		'name':	 					[MultiLanguageTextProxy,		True, 	None, 	'Human-readable name of designer'],
		'website':	 				[WebURLDataType,		False, 	None, 	'Designer’s web site'],
		'description':	 			[MultiLanguageTextProxy,		False, 	None, 	'Description of designer'],
	}

	def __repr__(self):
		return '<Designer "%s">' % self.name.getText() or self.keyword or 'undefined'

def Designer_Parent(self):
	if hasattr(self, '_parent') and hasattr(self._parent, '_parent') and hasattr(self._parent._parent, '_parent'):
		return self._parent._parent._parent
Designer.parent = property(lambda self: Designer_Parent(self))

class DesignerProxy(Proxy):
	dataType = Designer

class DesignersListProxy(ListProxy):
	dataType = DesignerProxy

class DesignersReferencesListProxy(ListProxy):
	dataType = UnicodeDataType

####################################################################################################################################

#  Font Family Version


class Version(DictBasedObject):
	# 	key: 					[data type, required, default value, description]
	_structure = {
		'number':	 				[VersionDataType,			True, 	None, 	'Font version number. This can be a simple float number (1.002) or a semver version string (see https://semver.org). For comparison, single-dot version numbers (or even integers) are appended with another .0 (1.0 to 1.0.0), then compared using the Python `semver` module.'],
		'description':	 			[MultiLanguageTextProxy,	False, 	None, 	'Description of font version'],
		'releaseDate':	 			[DateDataType,				False, 	None, 	'Font version’s release date.'],
	}

	def __repr__(self):
		return '<Version %s (%s)>' % (self.number if self.number else 'None', 'font-specific' if self.isFontSpecific() else 'family-specific')

	def isFontSpecific(self):
		'''\
		Returns True if this version is defined at the font level. Returns False if this version is defined at the family level.
		'''
		return issubclass(self.parent.__class__, Font)

def Version_Parent(self):
	if hasattr(self, '_parent') and hasattr(self._parent, '_parent') and hasattr(self._parent._parent, '_parent'):
		return self._parent._parent._parent
Version.parent = property(lambda self: Version_Parent(self))

class VersionProxy(Proxy):
	dataType = Version

class VersionListProxy(ListProxy):
	dataType = VersionProxy


####################################################################################################################################

#  Fonts

class Font(DictBasedObject):
	# 	key: 					[data type, required, default value, description]
	_structure = {
		'name':	 			[MultiLanguageTextProxy,		True, 	None, 	'Human-readable name of font. This may include any additions that you find useful to communicate to your users.'],
		'uniqueID':			[StringDataType,		True, 	None, 	'A machine-readable string that uniquely identifies this font within the publisher. It will be used to ask for un/installation of the font from the server in the `installFont` and `uninstallFont` commands. Also, it will be used for the file name of the font on disk, together with the version string and the file extension. Together, they must not be longer than 255 characters and must not contain the following characters: / ? < > \\ : * | ^'],
		'postScriptName':	[UnicodeDataType,		True, 	None, 	'Complete PostScript name of font'],
		'previewImage':		[WebURLDataType,		False, 	None, 	'URL of preview image of font, specifications to follow. %s' % WEBRESOURCEDESCRIPTION],
		'setName':			[MultiLanguageTextProxy,False, 	None, 	'Optional set name of font. This is used to group fonts in the UI. Think of fonts here that are of identical technical formats but serve different purposes, such as "Office Fonts" vs. "Desktop Fonts".'],
		'versions':	 		[VersionListProxy,		False, 	None, 	'List of ::Version:: objects. These are font-specific versions; they may exist only for this font. You may define additional versions at the family object under ::Family.versions::, which are then expected to be available for the entire family. However, either the fonts or the font family *must* carry version information and the validator will complain when they don’t.\n\nPlease also read the section on [versioning](#versioning) above.'],
		'designers':	 	[DesignersReferencesListProxy,	False, 	None, 	'List of keywords referencing designers. These are defined at ::InstallableFontsResponse.designers::. This attribute overrides the designer definitions at the family level at ::Family.designers::.'],
		'free':				[BooleanDataType,		False, 	None, 	'Font is freeware. For UI signaling'],
		'beta':				[BooleanDataType,		False, 	None, 	'Font is in beta stage. For UI signaling'],
		'variableFont':		[BooleanDataType,		False, 	None, 	'Font is an OpenType Variable Font. For UI signaling'],
		'purpose':			[FontTypeDataType,		True, 	None, 	'Technical purpose of font. This influences how the app handles the font. For instance, it will only install desktop fonts on the system, and make other font types available though folders. Possible: %s' % (list(FONTTYPES.keys()))],
		'format':			[FontExtensionDataType,	False, 	None, 	'Font file format. Required value in case of `desktop` font (see ::Font.purpose::. Possible: %s' % FILEEXTENSIONS],
		'protected':		[BooleanDataType,		False, 	False, 	'Indication that the server requires a valid subscriptionID to be used for authentication. The server *may* limit the downloads of fonts. This may also be used for fonts that are free to download, but their installations want to be tracked/limited anyway. Most importantly, this indicates that the uninstall command needs to be called on the API endpoint when the font gets uninstalled.'],
		'dateFirstPublished':[DateDataType,			False, 	None, 	'Date of the initial release of the font. May also be defined family-wide at ::Family.dateFirstPublished::.'],
		'usedLicenses':	 	[LicenseUsageListProxy,	True, 	None, 	'List of ::LicenseUsage:: objects. These licenses represent the different ways in which a user has access to this font. At least one used license must be defined here, because a user needs to know under which legal circumstances he/she is using the font. Several used licenses may be defined for a single font in case a customer owns several licenses that cover the same font. For instance, a customer could have purchased a font license standalone, but also as part of the foundry’s entire catalogue. It’s important to keep these separate in order to provide the user with separate upgrade links where he/she needs to choose which of several owned licenses needs to be upgraded. Therefore, in case of a commercial retail foundry, used licenses correlate to a user’s purchase history.'],
	}

	def __repr__(self):
		return '<Font "%s">' % (self.postScriptName or self.name.getText() or 'undefined')

	def filename(self, version):
		'''\
		Returns the recommended font file name to be used to store the font on disk.

		It is composed of the font’s uniqueID, its version string and the file extension. Together, they must not exceed 255 characters.
		'''
		if self.format:
			return '%s_%s.%s' % (self.uniqueID, version, self.format)
		else:
			return '%s_%s' % (self.uniqueID, version)

	def hasVersionInformation(self):
		return self.versions or self.parent.versions

	def customValidation(self):
		information, warnings, critical = [], [], []

		# Checking font type/extension
		if self.format == 'desktop' and not self.fileExtension:
			critical.append('The font %s is a desktop font (see .purpose), but has no .format value.' % (self))

		# Checking version information
		if not self.hasVersionInformation():
			critical.append('The font %s has no version information, and neither has its family %s. Either one needs to carry version information.' % (self, self.parent))

		# Checking for designers
		for designerKeyword in self.designers:
			if not self.parent.parent.parent.getDesignerByKeyword(designerKeyword):
				critical.append('%s has designer "%s", but %s.designers has no matching designer.' % (self, designerKeyword, self.parent.parent.parent))

		# Checking uniqueID for file name contradictions:
		forbidden = '/?<>\\:*|^'
		for char in forbidden:
			if self.uniqueID.count(char) > 0:
				critical.append("uniqueID must not contain the character %s because it will be used for the font's file name on disk." % char)

		for version in self.getVersions():
			if len(self.filename(version.number)) > 255:
				critical.append("The suggested file name is longer than 255 characters. It is composed of the font's uniqueID, its version string and the file extension like so: fontsUniqueID_1.2.otf")

		return information, warnings, critical

	def getVersions(self):
		'''\
		Returns list of ::Version:: objects.

		This is the final list based on the version information in this font object as well as in its parent ::Family:: object. Please read the section about [versioning](#versioning) above.
		'''

		if not self.hasVersionInformation():
			raise ValueError('Font %s has no version information, and neither has its family %s. Either one needs to carry version information.' % (self, self.parent))


		def compare(a, b):
			return semver.compare(makeSemVer(a.number), makeSemVer(b.number))

		versions = []
		haveVersionNumbers = []
		for version in self.versions:
			versions.append(version)
			haveVersionNumbers.append(makeSemVer(version.number))
		for version in self.parent.versions:
			if not version.number in haveVersionNumbers:
				versions.append(version)
				haveVersionNumbers.append(makeSemVer(version.number))

		versions = sorted(versions, key=functools.cmp_to_key(compare))

		return versions

	def getDesigners(self):
		'''\
		Returns a list of ::Designer:: objects that this font references. These are the combination of family-level designers and font-level designers. The same logic as for versioning applies. Please read the section about [versioning](#versioning) above.
		'''
		if not hasattr(self, '_designers'):
			self._designers = []

			# Family level designers
			if self.parent.designers:
				for designerKeyword in self.parent.designers:
					self._designers.append(self.parent.parent.parent.getDesignerByKeyword(designerKeyword))

			# Font level designers
			if self.designers:
				for designerKeyword in self.designers:
					self._designers.append(self.parent.parent.parent.getDesignerByKeyword(designerKeyword))

		return self._designers


def Font_Parent(self):
	if hasattr(self, '_parent') and hasattr(self._parent, '_parent') and hasattr(self._parent._parent, '_parent'):
		return self._parent._parent._parent
Font.parent = property(lambda self: Font_Parent(self))


class FontProxy(Proxy):
	dataType = Font

class FontListProxy(ListProxy):
	dataType = FontProxy


# Font Family

class BillboardListProxy(ListProxy):
	dataType = WebURLDataType

class Family(DictBasedObject):
	# 	key: 					[data type, required, default value, description]
	_structure = {
		'uniqueID':					[StringDataType,		True, 	None, 	'An string that uniquely identifies this family within the publisher.'],
		'name':	 					[MultiLanguageTextProxy,True, 	None, 	'Human-readable name of font family. This may include any additions that you find useful to communicate to your users.'],
		'description':	 			[MultiLanguageTextProxy,False, 	None, 	'Description of font family'],
		'billboards':	 			[BillboardListProxy,	False, 	None, 	'List of URLs pointing at images to show for this typeface, specifications to follow'],
		'designers':	 			[DesignersReferencesListProxy,	False, 	None, 	'List of keywords referencing designers. These are defined at ::InstallableFontsResponse.designers::. In case designers differ between fonts within the same family, they can also be defined at the font level at ::Font.designers::. The font-level references take precedence over the family-level references.'],

		'sourceURL':	 			[WebURLDataType,		False, 	None, 	'URL pointing to the source of a font project, such as a GitHub repository'],
		'issueTrackerURL':	 		[WebURLDataType,		False, 	None, 	'URL pointing to an issue tracker system, where users can debate about a typeface’s design or technicalities'],
		'versions':	 				[VersionListProxy,		False, 	None, 	'List of ::Version:: objects. Versions specified here are expected to be available for all fonts in the family, which is probably most common and efficient. You may define additional font-specific versions at the ::Font:: object. You may also rely entirely on font-specific versions and leave this field here empty. However, either the fonts or the font family *must* carry version information and the validator will complain when they don’t.\n\nPlease also read the section on [versioning](#versioning) above.'],
		'fonts':	 				[FontListProxy,			True, 	None, 	'List of ::Font:: objects. The order will be displayed unchanged in the UI, so it’s in your responsibility to order them correctly.'],
		'dateFirstPublished':		[DateDataType,			False, 	None, 	'Date of the initial release of the family. May be overriden on font level at ::Font.dateFirstPublished::.'],
	}

	def __repr__(self):
		return '<Family "%s">' % self.name.getText() or 'undefined'

	def customValidation(self):
		information, warnings, critical = [], [], []

		# Checking for designers
		for designerKeyword in self.designers:
			if not self.parent.parent.getDesignerByKeyword(designerKeyword):
				critical.append('%s has designer "%s", but %s.designers has no matching designer.' % (self, designerKeyword, self.parent.parent))

		return information, warnings, critical

	def getDesigners(self):
		if not hasattr(self, '_designers'):
			self._designers = []
			for designerKeyword in self.designers:
				self._designers.append(self.parent.parent.getDesignerByKeyword(designerKeyword))
		return self._designers

	def getAllDesigners(self):
		'''\
		Returns a list of ::Designer:: objects that represent all of the designers referenced both at the family level as well as with all the family’s fonts, in case the fonts carry specific designers. This could be used to give a one-glance overview of all designers involved.
		'''
		if not hasattr(self, '_allDesigners'):
			self._allDesigners = []
			self._allDesignersKeywords = []
			for designerKeyword in self.designers:
				self._allDesigners.append(self.parent.parent.getDesignerByKeyword(designerKeyword))
				self._allDesignersKeywords.append(designerKeyword)
			for font in self.fonts:
				for designerKeyword in font.designers:
					if not designerKeyword in self._allDesignersKeywords:
						self._allDesigners.append(self.parent.parent.getDesignerByKeyword(designerKeyword))
						self._allDesignersKeywords.append(designerKeyword)
		return self._allDesigners

def Family_Parent(self):
	if hasattr(self, '_parent') and hasattr(self._parent, '_parent') and hasattr(self._parent._parent, '_parent'):
		return self._parent._parent._parent
Family.parent = property(lambda self: Family_Parent(self))

class FamilyProxy(Proxy):
	dataType = Family

class FamiliesListProxy(ListProxy):
	dataType = FamilyProxy


####################################################################################################################################

#  Font Foundry

class Foundry(DictBasedObject):
	# 	key: 					[data type, required, default value, description]
	_structure = {
		'uniqueID':					[StringDataType,		True, 	None, 	'An string that uniquely identifies this foundry within the publisher.'],
		'name':	 					[MultiLanguageTextProxy,True, 	None, 	'Name of foundry'],
		'logo':	 					[WebURLDataType,		False, 	None, 	'URL of foundry’s logo. Specifications to follow. %s' % WEBRESOURCEDESCRIPTION],
		'description':	 			[MultiLanguageTextProxy,False, 	None, 	'Description of foundry'],
		'email':	 				[EmailDataType,			False, 	None, 	'General email address for this foundry'],
		'supportEmail':	 			[EmailDataType,			False, 	None, 	'Support email address for this foundry'],
		'website':	 				[WebURLDataType,		False, 	None, 	'Website for this foundry'],
		'twitter':	 				[UnicodeDataType,		False, 	None, 	'Twitter handle for this foundry, without the @'],
		'facebook':	 				[WebURLDataType,		False, 	None, 	'Facebook page URL handle for this foundry. The URL '],
		'instagram':	 			[UnicodeDataType,		False, 	None, 	'Instagram handle for this foundry, without the @'],
		'skype':	 				[UnicodeDataType,		False, 	None, 	'Skype handle for this foundry'],
		'telephone':	 			[UnicodeDataType,		False, 	None, 	'Telephone number for this foundry'],

		#styling
		'backgroundColor': 			[HexColorDataType,		False, 	None, 	'Foundry’s preferred background color. This is meant to go as a background color to the logo at ::Foundry.logo::'],

		# data
		'licenses':					[LicenseDefinitionListProxy,True, 	None, 	'List of ::LicenseDefinition:: objects under which the fonts in this response are issued. For space efficiency, these licenses are defined at the foundry object and will be referenced in each font by their keyword. Keywords need to be unique for this foundry and may repeat across foundries.'],
		'families':					[FamiliesListProxy,		True, 	None, 	'List of ::Family:: objects.'],
	}

	def __repr__(self):
		return '<Foundry "%s">' % self.name.getText() or 'undefined'

	def getLicenseByKeyword(self, keyword):
		if not hasattr(self, '_licensesDict'):
			self._licensesDict = {}
			for license in self.licenses:
				self._licensesDict[license.keyword] = license

		if keyword in self._licensesDict:
			return self._licensesDict[keyword]


def Foundry_Parent(self):
	if hasattr(self, '_parent') and hasattr(self._parent, '_parent') and hasattr(self._parent._parent, '_parent'):
		return self._parent._parent._parent
Foundry.parent = property(lambda self: Foundry_Parent(self))

class FoundryProxy(Proxy):
	dataType = Foundry

class FoundryListProxy(ListProxy):
	dataType = FoundryProxy

####################################################################################################################################

#  Available Fonts

class BaseResponse(DictBasedObject):
	# 	key: 					[data type, required, default value, description]
	_base_structure = {
	}

	def __repr__(self):
		return '<%s>' % self.__class__.__name__


	def customValidation(self):
		information, warnings, critical = [], [], []

		if self.type == ERROR and self.errorMessage is None:
			warnings.append('%s.type is "%s", but .errorMessage is missing.' % (self, ERROR))

		return information, warnings, critical

def BaseResponse_Parent(self):
	if hasattr(self, '_parent') and hasattr(self._parent, '_parent'):
		return self._parent._parent
BaseResponse.parent = property(lambda self: BaseResponse_Parent(self))


class InstallableFontsResponseType(UnicodeDataType):
	def valid(self):
		if self.value in INSTALLABLEFONTSCOMMAND['responseTypes']:
			return True
		else:
			return 'Unknown response type: "%s". Possible: %s' % (self.value, INSTALLABLEFONTSCOMMAND['responseTypes'])

class InstallableFontsResponse(BaseResponse):
	'''\
	This is the response expected to be returned when the API is invoked using the command parameter, such as `http://fontpublisher.com/api/?command=installableFonts`.

	The response needs to be specified at the ::Response.command:: attribute, and then the ::Response:: object needs to carry the specific response command at the attribute of same name, in this case ::Reponse.installableFonts::.

	```python
	api.response = Response()
	api.response.command = 'installableFonts'
	api.response.installableFonts = InstallableFontsResponse()
	```

	'''
	# 	key: 					[data type, required, default value, description]
	_structure = {

		# Root
		'type': 			[InstallableFontsResponseType,	True, 	None, 	'Type of response. This can be "success", "error", or "custom". In case of "custom", you may specify an additional message to be presented to the user under ::InstallableFontsResponse.errorMessage::.'],
		'errorMessage': 	[MultiLanguageTextProxy,				False, 	None, 	'Description of error in case of ::InstallableFontsResponse.type:: being "custom".'],
		'version': 			[FloatDataType,					True, 	INSTALLABLEFONTSCOMMAND['currentVersion'], 	'Version of "%s" response' % INSTALLABLEFONTSCOMMAND['keyword']],

		# Response-specific
		'designers':		[DesignersListProxy,			False, 	None, 	'List of ::Designer:: objects, referenced in the fonts or font families by the keyword. These are defined at the root of the response for space efficiency, as one designer can be involved in the design of several typefaces across several foundries.'],
		'foundries':		[FoundryListProxy,				True, 	None, 	'List of ::Foundry:: objects; foundries that this distributor supports. In most cases this will be only one, as many foundries are their own distributors.'],

		'name':			[MultiLanguageTextProxy,		False, 	None, 	'A name of this response and its contents. This is needed to manage subscriptions in the UI. For instance "Free Fonts" for all free and non-restricted fonts, or "Commercial Fonts" for all those fonts that the use has commercially licensed, so their access is restricted. In case of a free font website that offers individual subscriptions for each typeface, this decription could be the name of the typeface.'],
		'userName':			[MultiLanguageTextProxy,		False, 	None, 	'The name of the user who these fonts are licensed to.'],
		'userEmail':		[EmailDataType,					False, 	None, 	'The email address of the user who these fonts are licensed to.'],
	}


	def getDesignerByKeyword(self, keyword):
		if not hasattr(self, '_designersDict'):
			self._designersDict = {}
			for designer in self.designers:
				self._designersDict[designer.keyword] = designer

		if keyword in self._designersDict:
			return self._designersDict[keyword]

	def discardThisKey(self, key):
		
		if key in ['foundries', 'designers', 'licenseIdentifier'] and self.type == 'error':
			return True

		return False

	def customValidation(self):
		information, warnings, critical = [], [], []

		if self.type == 'success' and not self.name.getText():
			warnings.append('The response has no .name value. It is not required, but highly recommended, to describe the purpose of this subscription to the user (such as "Commercial Fonts", "Free Fonts", etc. This is especially useful if you offer several different subscriptions to the same user.')


		# Check all uniqueIDs for duplicity
		foundryIDs = []
		familyIDs = []
		fontIDs = []
		for foundry in self.foundries:
			foundryIDs.append(foundry.uniqueID)
			for family in foundry.families:
				familyIDs.append(family.uniqueID)
				for font in family.fonts:
					fontIDs.append(font.uniqueID)

		import collections

		duplicateFoundryIDs = [item for item, count in list(collections.Counter(foundryIDs).items()) if count > 1]
		if duplicateFoundryIDs:
			critical.append('Duplicate unique foundry IDs: %s' % duplicateFoundryIDs)

		duplicateFamilyIDs = [item for item, count in list(collections.Counter(familyIDs).items()) if count > 1]
		if duplicateFamilyIDs:
			critical.append('Duplicate unique family IDs: %s' % duplicateFamilyIDs)

		duplicateFontIDs = [item for item, count in list(collections.Counter(fontIDs).items()) if count > 1]
		if duplicateFontIDs:
			critical.append('Duplicate unique family IDs: %s' % duplicateFontIDs)


		return information, warnings, critical





class InstallableFontsResponseProxy(Proxy):
	dataType = InstallableFontsResponse

####################################################################################################################################

#  InstallFont

class InstallFontResponseType(UnicodeDataType):
	def valid(self):
		if self.value in INSTALLFONTCOMMAND['responseTypes']:
			return True
		else:
			return 'Unknown response type: "%s". Possible: %s' % (self.value, INSTALLFONTCOMMAND['responseTypes'])

class InstallFontResponse(BaseResponse):
	# 	key: 					[data type, required, default value, description]
	_structure = {

		# Root
		'type': 			[InstallFontResponseType,	True, 	None, 	'Success or error.'],
		'errorMessage': 	[MultiLanguageTextProxy,		False, 	None, 	'Description of error in case of custom response type'],
		'version': 			[FloatDataType,					True, 	INSTALLFONTCOMMAND['currentVersion'], 	'Version of "%s" response' % INSTALLFONTCOMMAND['keyword']],

		'font': 			[FontDataType,				False, 	None, 	'Binary font data encoded to a string using ::InstallFontResponse.encoding::'],
		'encoding': 		[FontEncodingDataType,		False, 	None, 	'Encoding type for binary font data. Currently supported: %s' % (FONTENCODINGS)],
		'fileName':			[UnicodeDataType, 			False, 	None, 	'Suggested file name of font. This may be ignored by the app in favour of a unique file name.'],

		# Response-specific
		}

	def customValidation(self):

		information, warnings, critical = [], [], []

		if self.type == 'success' and not self.font:
			critical.append('%s.type is set to success, but %s.font is missing' % (self, self))

		if self.font and not self.encoding:
			critical.append('%s.font is set, but %s.encoding is missing' % (self, self))

		return information, warnings, critical


class InstallFontResponseProxy(Proxy):
	dataType = InstallFontResponse

####################################################################################################################################

#  Uninstall Fonts

class UninstallFontResponseType(UnicodeDataType):
	def valid(self):
		if self.value in UNINSTALLFONTCOMMAND['responseTypes']:
			return True
		else:
			return 'Unknown response type: "%s". Possible: %s' % (self.value, UNINSTALLFONTCOMMAND['responseTypes'])

class UninstallFontResponse(BaseResponse):
	# 	key: 					[data type, required, default value, description]
	_structure = {

		# Root
		'type': 			[UninstallFontResponseType,	True, 	None, 	'Success or error.'],
		'errorMessage': 	[MultiLanguageTextProxy,		False, 	None, 	'Description of error in case of custom response type'],
		'version': 			[FloatDataType,					True, 	UNINSTALLFONTCOMMAND['currentVersion'], 	'Version of "%s" response' % UNINSTALLFONTCOMMAND['keyword']],

		# Response-specific
		}

class UninstallFontResponseProxy(Proxy):
	dataType = UninstallFontResponse


class Response(DictBasedObject):
	# 	key: 					[data type, required, default value, description]
	_structure = {
		'command': 							[SupportedAPICommandsDataType,	True, 	None, 	'Command code of the response. The specific response must then be present under an attribute of same name.'],
		INSTALLABLEFONTSCOMMAND['keyword']:	[InstallableFontsResponseProxy, 	False, 	None, 	''],
		INSTALLFONTCOMMAND['keyword']:		[InstallFontResponseProxy, 	False, 	None, 	''],
		UNINSTALLFONTCOMMAND['keyword']:	[UninstallFontResponseProxy, 	False, 	None, 	''],
	}

	def __repr__(self):
		return '<Response>'

	def getCommand(self):
		'''\
Returns the specific response referenced in the .command attribute. This is a shortcut.

```python
print api.response.getCommand()

# will print:
<InstallableFontsResponse>

# which is the same as:
print api.response.get(api.response.command)

# will print:
<InstallableFontsResponse>
```
'''
#		exec("command = self.%s" % self.command)
		return self.get(self.command)

	def customValidation(self):

		information, warnings, critical = [], [], []

		if not self.getCommand():
			critical.append('%s.command is set, but we are missing that command at %s.%s' % (self, self, self.command))

		return information, warnings, critical


def Response_Parent(self):
	if hasattr(self, '_parent') and hasattr(self._parent, '_parent'):
		return self._parent._parent
Response.parent = property(lambda self: Response_Parent(self))


class ResponseProxy(Proxy):
	dataType = Response

class APIRoot(DictBasedObject):
	'''\
This is the main class that sits at the root of all API responses. It contains some mandatory information about the API endpoint such as its name and admin email, the copyright license under which the API endpoint issues its data, and whether or not this endpoint can be publicized about.

Any API response is expected to carry this minimum information, even when invoked without a particular command.

In case the API endpoint has been invoked with a particular command, the response data is attached to the ::APIRoot.response:: attribute.


```python
api = APIRoot()
api.name.en = u'Font Publisher'
api.canonicalURL = 'https://fontpublisher.com/api/'
api.adminEmail = 'admin@fontpublisher.com'
api.supportedCommands = ['installableFonts', 'installFonts', 'uninstallFonts']
```

	'''


	# 	key: 					[data type, required, default value, description]
	_structure = {
		'canonicalURL': 		[WebURLDataType, 			True, 	None, 	'Official API endpoint URL, bare of ID keys and other parameters. Used for grouping of subscriptions. It is expected that this URL will not change. When it does, it will be treated as a different publisher.'],
		'adminEmail': 			[EmailDataType, 			True, 	None, 	'API endpoint Administrator. This email needs to be reachable for various information around the Type.World protocol as well as technical problems.'],
		'licenseIdentifier':	[OpenSourceLicenseIdentifierDataType,True, 	'CC-BY-NC-ND-4.0', 	'Identifier of license under which the API endpoint publishes its data, as per [https://spdx.org/licenses/](). This license will not be presented to the user. The software client needs to be aware of the license and proceed only if allowed, otherwise decline the usage of this API endpoint. Licenses of the individual responses can be fine-tuned in the respective responses.'],
		'supportedCommands': 	[SupportedAPICommandsListProxy, True, 	None, 	'List of commands this API endpoint supports: %s' % [x['keyword'] for x in COMMANDS]],
		'name': 				[MultiLanguageTextProxy, 	True, 	None, 	'Human-readable name of API endpoint'],
		'public': 				[BooleanDataType, 			True, 	False, 	'API endpoint is meant to be publicly visible and its existence may be publicized within the project'],
		'logo': 				[WebURLDataType, 			False, 	None, 	'URL of logo of API endpoint, for publication. Specifications to follow. %s' % WEBRESOURCEDESCRIPTION],
		'backgroundColor': 		[HexColorDataType,			False, 	None, 	'Publisher’s preferred background color. This is meant to go as a background color to the logo at ::APIRoot.logo::'],
		'website': 				[WebURLDataType, 			False, 	None, 	'URL of human-visitable website of API endpoint, for publication'],
		'response': 			[ResponseProxy, 			False, 	None, 	'Response of the API call'],
	}

	def difference(self, other):
		from deepdiff import DeepDiff
		return DeepDiff(self.dumpDict(), other.dumpDict(), ignore_order=True)

	def sameContent(self, other):
		'''\
		Compares the data structure of this object to the other object.

		Requires deepdiff module.
		'''
		return self.difference(other) == {}


	def __repr__(self):
		return '<API>'

	def validate(self):
		'''\
		Return three lists with informations, warnings, and errors.

		An empty errors list is regarded as a successful validation, otherwise the validation is regarded as a failure.
		'''
		information, warnings, errors = self._validate()

		if self.canonicalURL and not self.canonicalURL.startswith('https://'):
			warnings.append('%s.canonicalURL is not using SSL (https://). Consider using SSL to protect your data.' % (self))

		return information, warnings, errors



