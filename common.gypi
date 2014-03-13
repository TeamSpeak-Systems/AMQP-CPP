{ 'target_defaults':
  {

   'variables': {
	'conditions': [
        ['OS=="win" and runtime=="shared"', {
          # See http://msdn.microsoft.com/en-us/library/aa652367.aspx
          'win_release_RuntimeLibrary%': '2', # 2 = /MD (nondebug DLL)
          'win_debug_RuntimeLibrary%': '3',   # 3 = /MDd (debug DLL)
		 }],
		 [ 'OS=="win" and runtime=="static"', {
          # See http://msdn.microsoft.com/en-us/library/aa652367.aspx
          'win_release_RuntimeLibrary%': '0', # 0 = /MT (nondebug static)
          'win_debug_RuntimeLibrary%': '1',   # 1 = /MTd (debug static)
        }],
      ],
  },
 
	'msvs_configuration_attributes' : {
		'OutputDirectory' : '$(SolutionDir)build\\$(Platform)\\$(Configuration)\\$(ProjectName)\\',
		'IntermediateDirectory' : '$(SolutionDir)build\\$(Platform)\\$(Configuration)\\$(ProjectName)\\obj\\',
	},
    'msbuild_toolset': 'v110_xp',
    'default_configuration': 'Release',
    'configurations':
	{
      'Debug':
	  {
        'defines': [ 'DEBUG', '_DEBUG' ],
        'msvs_settings':
		{
          'VCCLCompilerTool':
		  {
            'AdditionalIncludeDirectories': ['/projects/msvc2012/$(PlatformArchitecture)/>(runtime)/include'],
            'RuntimeLibrary': '>(win_debug_RuntimeLibrary)',
			'BasicRuntimeChecks' : 3,
			'Optimization': 0,
          },
          'VCLinkerTool':
		  {
            'AdditionalLibraryDirectories':[ '/projects/msvc2012/$(PlatformArchitecture)/>(runtime)/lib'],
            'LinkTimeCodeGeneration': 1,
            'OptimizeReferences': 2,
            'EnableCOMDATFolding': 2,
            'LinkIncremental': 1,
            'GenerateDebugInformation': 'true'
          }          
        },
        'xcode_settings':
		{
          #'OTHER_LDFLAGS':
		  #[
          #  '-Lexternal/thelibrary/lib/debug'
          #]
        }
      },
	  'Release':
	  {
        'defines': [ 'NDEBUG' ],
        'msvs_settings':
		{
          'VCCLCompilerTool':
		  {
            'AdditionalIncludeDirectories': ['/projects/msvc2012/$(PlatformArchitecture)/>(runtime)/include'],
            'RuntimeLibrary': '>(win_release_RuntimeLibrary)',
            'Optimization': 3,
            'FavorSizeOrSpeed': 1,
            'InlineFunctionExpansion': 2,
            'WholeProgramOptimization': 'true',
            'OmitFramePointers': 'true',
            'EnableFunctionLevelLinking': 'true',
            'EnableIntrinsicFunctions': 'true'            
          },
          'VCLinkerTool':
		  {
            'AdditionalLibraryDirectories':[ '/projects/msvc2012/$(PlatformArchitecture)/>(runtime)/lib'],
            'LinkTimeCodeGeneration': 1,
            'OptimizeReferences': 2,
            'EnableCOMDATFolding': 2,
            'LinkIncremental': 1,
          }          
        },
        'xcode_settings':
		{
         'OTHER_LDFLAGS':
		 [
              '-Lexternal/thelibrary/lib/release'
         ]
        }
      }
    }  
  }
}