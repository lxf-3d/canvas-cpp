
import os.path

top = '.'
out = 'build'

SOURCE = """
   src/ColorParser.cpp
   src/Canvas.cpp
   src/Context.cpp
   src/Script.cpp
   src/Painter.cpp
   src/binding/Object.cpp
   src/util/Thread.cpp
   src/util/Mutex.cpp
   src/util/ScopedLock.cpp
""".split()

TESTS = """
   tests/Main.cpp
   tests/ColorParserTest.cpp
""".split()

def files_exists(files, path):
   for file in files:
      if os.path.exists(os.path.join(path, file)):
         return True
   return False

def set_options(conf):
   conf.add_option('--skia-include', action='store', default=None, help="Search path to Skia include path.")
   conf.add_option('--skia-lib', action='store', default=None, help="Search path to Skia lib path.")
   conf.add_option('--v8-include', action='store', default=None, help="Search path to V8 include path.")
   conf.add_option('--v8-lib', action='store', default=None, help="Search path to V8 lib path.")

def configure(conf):
   import Options
   conf.check_tool('g++')
   
   conf.env.CANVAS_DEFINES = []
   
   if conf.check(lib='pthread', uselib_store='pthread', mandatory=True):
      conf.env.CANVAS_DEFINES.extend('CANVAS_USE_PTHREAD')
   
   if Options.options.skia_include == None:
      conf.fatal("Missing Skia include path!")
   if Options.options.skia_lib == None:
      conf.fatal("Missing Skia lib path!")
   if Options.options.v8_include == None:
      conf.fatal("Missing V8 include path!")
   if Options.options.v8_lib == None:
      conf.fatal("Missing V8 lib path!")
   
   conf.env.SKIA_INCLUDE = Options.options.skia_include
   conf.env.SKIA_LIB = Options.options.skia_lib
   conf.env.V8_INCLUDE = Options.options.v8_include
   conf.env.V8_LIB = Options.options.v8_lib
   
   # Check that we have access to both Skia and V8.
   skiaHeaderExists = files_exists([os.path.join('core', 'SkCanvas.h')], conf.env.SKIA_INCLUDE)
   skiaLibraryExists = files_exists(['libskia.a', 'libskia.so', 'libskia.lib'], conf.env.SKIA_LIB)
   v8HeaderExists = files_exists(['v8.h'], conf.env.V8_INCLUDE)
   v8LibraryExists = files_exists(['libv8.a', 'libv8.so', 'libv8.lib'], conf.env.V8_LIB)
   
   conf.check_message('header', 'SkCanvas.h', skiaHeaderExists)
   conf.check_message('header', 'v8.h', v8HeaderExists)
   conf.check_message('library', 'libskia', skiaLibraryExists)
   conf.check_message('library', 'libv8', v8LibraryExists)
   
   if not (skiaHeaderExists and skiaLibraryExists and v8HeaderExists and v8LibraryExists):
      conf.fatal("Could not find required dependencies!")
   
def build(bld):
   canvas_lib = bld(
      features = 'cxx cstaticlib',
      target = 'canvas',
      source = SOURCE,
      defines = [],
      includes = ['src', 'src/binding', 'include', bld.env.SKIA_INCLUDE, bld.env.V8_INCLUDE],
      uselib = 'pthread',
      staticlib = 'skia v8',
      libpath = [bld.env.SKIA_LIB, bld.env.V8_LIB])
      
   tests = bld(
      features = "cxx cprogram",
      target = 'unit_tests',
      source = TESTS,
      uselib_local = "canvas",
      unit_test = 1,
      includes = ['include', 'tests'])

