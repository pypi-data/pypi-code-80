"PS：蓝色顶级文件夹:RootBlueFolderName，扫描无法区分---通过配置文件手动告知有哪些"

"PBXBuildFile = PBXSourcesBuildPhase + PBXResourcesBuildPhase + PBXFrameworksBuildPhase + RootBlueFolderName"
# /* Begin PBXBuildFile section */

"PBXFileReference = PBXBuildFile + 所有的.h文件"
# /* Begin PBXFileReference section */

"xCode中的Build Phases-->Link Binary With Libraries = 项目中的.a文件 + 项目中Frameworks文件夹下的所有"
# /* Begin PBXFrameworksBuildPhase section */

"""添加到了项目工程中的所有文件 + RootBlueFolderName
   其实就是拖文件到xCode中，通过Create groups导进去的。
"""
# /* Begin PBXGroup section */

"这里修改项目名字"
# /* Begin PBXNativeTarget section */

"这个不用管，里面有项目名字符串需要替换"
# /* Begin PBXProject section */

"""Build Phases-->Copy Bundle Resources，所有打包到xxx.bundle中的内容
   .png, .plist, xib, .storyboard, json等非代码文件(除了特殊的info.plist)"""
# /* Begin PBXResourcesBuildPhase section */

"Build Phases-->Compile Sources，所以编译成xxx.a静态库的.m代码"
# /* Begin PBXSourcesBuildPhase section */ 参与编译的代码，新增垃圾代码加到这里。

"国家化语言相关，原封不动"
# /* Begin PBXVariantGroup section */

"对应Xcode中 Build Settings中的配置信息，原封不动"
# /* Begin XCBuildConfiguration section */  配置文件，不管

"原封不动"
# /* Begin XCConfigurationList section */  Debug or Release