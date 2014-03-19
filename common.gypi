{
   'variables': {
	'visibility%': 'hidden',         # visibility setting
    'target_arch%': 'x86',          # set target architecture
    'host_arch%': 'x86',            # set host architecture
    'library%': 'static_library',    # allow override to 'shared_library' for DLL/.so builds
    'msvs_multi_core_compile': 'true',  # we do enable multicore compiles
	'subsystem%': 'console',
  },

 'target_defaults':
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
		['target_arch=="x86"', { 'target_bits' : 32 }],
		['target_arch=="x64"', { 'target_bits' : 64 }],
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
		'cflags': [ '-g', '-O0', '-fno-stack-protector', '-std=c11' ],
		'cflags_cc': [ '-g', '-O0', '-fno-stack-protector', '-std=c++11'],
		'conditions': [
          ['target_arch=="x64"', {
            'msvs_configuration_platform': 'x64',
          }],
        ],
        'msvs_settings':
		{
          'VCCLCompilerTool':
		  {
            'AdditionalIncludeDirectories': ['\\projects\\msvc2012\\>(target_bits)\\>(runtime)\\include'],
            'RuntimeLibrary': '>(win_debug_RuntimeLibrary)',
			'BasicRuntimeChecks' : 3,
			'Optimization': 0,
			'MinimalRebuild': 'true',
            'OmitFramePointers': 'false',
          },
          'VCLinkerTool':
		  {
            'AdditionalLibraryDirectories':[ '\\projects\\msvc2012\\>(target_bits)\\>(runtime)\\lib'],
            'LinkTimeCodeGeneration': 1,
            'OptimizeReferences': 2,
            'EnableCOMDATFolding': 2,
            'LinkIncremental': 2,
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
		'cflags': [ '-g', '-O2', '-fno-stack-protector', '-std=c11' ],
		'cflags_cc': [ '-g', '-O2', '-fno-stack-protector', '-std=c++11'],
		'conditions': [
          ['target_arch=="x64"', {
            'msvs_configuration_platform': 'x64',
          }],
        ],
        'msvs_settings':
		{
          'VCCLCompilerTool':
		  {
            'AdditionalIncludeDirectories': ['\\projects\\msvc2012\\>(target_bits)\\>(runtime)\\include'],
            'RuntimeLibrary': '>(win_release_RuntimeLibrary)',
            'Optimization': 3,
            'FavorSizeOrSpeed': 1,
            'InlineFunctionExpansion': 2,
            'WholeProgramOptimization': 'true',
            'OmitFramePointers': 'true',
            'EnableFunctionLevelLinking': 'true',
            'EnableIntrinsicFunctions': 'true'            
          },
		  'VCLibrarianTool': {
            'AdditionalOptions': [
              '/LTCG', # link time code generation
            ],
          },
          'VCLinkerTool':
		  {
            'AdditionalLibraryDirectories':[ '\\projects\\msvc2012\\PlatformArchitecture\\>(runtime)\\lib'],
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
    }  ,
  
  'msvs_settings': {
      'VCCLCompilerTool': {
        'StringPooling': 'true', # pool string literals
        'DebugInformationFormat': 3, # Generate a PDB
        'WarningLevel': 3,
        'BufferSecurityCheck': 'true',
        'ExceptionHandling': 1, # /EHsc
        'SuppressStartupBanner': 'true',
        'WarnAsError': 'false',
		'AdditionalOptions' :'-D_USING_V110_SDK71_', #needed for xp compatibility
#		'MultiProcessorCompilation' : '<(msvs_multi_core_compile)',
      },
      'VCLibrarianTool': {
      },
      'VCLinkerTool': {
        'conditions': [
          ['target_arch=="x64"', {
            'TargetMachine' : 17, # /MACHINE:X64
			'MinimumRequiredVersion': '5.02', #needed for xp compatibility
          }],
          ['target_arch=="x86"', {
			'MinimumRequiredVersion': '5.01', #needed for xp compatibility
          }],
        ],
        'GenerateDebugInformation': 'true',
        'RandomizedBaseAddress': 2, # enable ASLR
        'DataExecutionPrevention': 2, # enable DEP
        'AllowIsolation': 'true',
        'SuppressStartupBanner': 'true',
#        'target_conditions': [
#          ['_type=="executable"', {
#            'SubSystem': 1, # console executable
#          }],
#        ],
      },
    },
  
  
  'conditions': [
      ['OS == "win"', {
        'msvs_cygwin_shell': 0, # prevent actions from trying to use cygwin
        'defines': [
          'WIN32',
          # we don't really want VC++ warning us about
          # how dangerous C functions are...
		  '_SCL_SECURE_NO_WARNINGS',
          '_CRT_SECURE_NO_DEPRECATE',
          # ... or that C implementations shouldn't use
          # POSIX names
          '_CRT_NONSTDC_NO_DEPRECATE',
        ],
      }],
      [ 'OS=="linux" or OS=="freebsd"', {
        'cflags': [ '-Wall', '-pthread', ],
        'cflags_cc': [ '-Wall', '-pthread',],
        'ldflags': [ '-pthread', ],
        'conditions': [
          [ 'target_arch=="x86"', {
            'cflags': [ '-m32' ],
            'ldflags': [ '-m32' ],
          }],
          [ 'OS=="linux"', {
            'cflags': [  ],
            'ldflags': [  ],
          }],
        ],
      }],
      ['OS=="mac"', {
        'xcode_settings': {
          'ALWAYS_SEARCH_USER_PATHS': 'NO',
          'GCC_CW_ASM_SYNTAX': 'NO',                # No -fasm-blocks
          'GCC_DYNAMIC_NO_PIC': 'NO',               # No -mdynamic-no-pic
                                                    # (Equivalent to -fPIC)
          'GCC_ENABLE_CPP_EXCEPTIONS': 'YES',       # -fno-exceptions
          'GCC_ENABLE_CPP_RTTI': 'YES',             # -fno-rtti
          'GCC_ENABLE_PASCAL_STRINGS': 'NO',        # No -mpascal-strings
          'GCC_THREADSAFE_STATICS': 'NO',           # -fno-threadsafe-statics
          'GCC_VERSION': '4.7',
          'GCC_WARN_ABOUT_MISSING_NEWLINE': 'YES',  # -Wnewline-eof
          'PREBINDING': 'NO',                       # No -Wl,-prebind
          'USE_HEADERMAP': 'NO',
          'OTHER_CFLAGS': [
            '-fno-strict-aliasing',
          ],
          'WARNING_CFLAGS': [
            '-Wall',
            '-Wendif-labels',
            '-W',
            '-Wno-unused-parameter',
          ],
        },
        'target_conditions': [
          ['_type!="static_library"', {
            'xcode_settings': {'OTHER_LDFLAGS': ['-Wl,-search_paths_first']},
          }],
        ],
        'conditions': [
          ['target_arch=="x86"', {
            'xcode_settings': {'ARCHS': ['i386']},
          }],
          ['target_arch=="x64"', {
            'xcode_settings': {'ARCHS': ['x86_64']},
          }],
        ],
      }],
    ]
  
  
  
  
  
  },
  
  
  
  
  
  
  
}