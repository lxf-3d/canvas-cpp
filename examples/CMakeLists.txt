
SET(SOURCE 
  Demo.cpp
)

SET(LIBRARIES
  canvas
  skia
  v8
  ${SDL_LIBRARY}
  ${SDLIMAGE_LIBRARY}
)
              
IF(APPLE)
  LIST(APPEND SOURCE SDLMain.m)
  LIST(APPEND LIBRARIES ${Carbon_FRAMEWORK})
  LIST(APPEND LIBRARIES ${Cocoa_FRAMEWORK})
ENDIF()

ADD_EXECUTABLE(demo ${SOURCE})
TARGET_LINK_LIBRARIES(demo ${LIBRARIES})