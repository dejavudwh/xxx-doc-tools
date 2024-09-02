cmake_minimum_required(VERSION 3.10)
project(diff-pdf VERSION 0.5.2 LANGUAGES CXX)

# Find Poppler
find_package(PkgConfig REQUIRED)
pkg_check_modules(POPPLER REQUIRED glib-2.0>=2.36 poppler-glib>=0.10 cairo-pdf)

# set(CMAKE_PREFIX_PATH /d/msys64/mingw64/)
# Find wxWidgets
# find_package(wxWidgets COMPONENTS core base aui REQUIRED)
set(wxWidgets_INCLUDE_DIRS /d/msys64/mingw64/include/wx-3.0/
                           /d/msys64/mingw64/lib/wx/include/msw-unicode-3.0/)
set(wxWidgets_LIBRARY_DIRS /d/msys64/mingw64/bin/wx)
set(wxWidgets_LDFLAG --subsystem,windows)

# Set the source files
set(UED_DOC_TOOLS_SOURCES
    diff-pdf.cpp
    bmpviewer.cpp
    gutter.cpp
)

set(UED_DOC_TOOLS_HEADERS
    bmpviewer.h
    gutter.h
)

# Create the executable
# add_executable(ued_doc_tools ${UED_DOC_TOOLS_SOURCES} ${UED_DOC_TOOLS_HEADERS})
add_library(diff-pdf SHARED ${UED_DOC_TOOLS_SOURCES} ${UED_DOC_TOOLS_HEADERS})

# Include directories
target_include_directories(diff-pdf PRIVATE ${POPPLER_INCLUDE_DIRS} ${wxWidgets_INCLUDE_DIRS})
# Link libraries
add_link_options(${wxWidgets_LDFLAG})
link_directories(${wxWidgets_LIBRARY_DIRS})
file(GLOB wxWidgets_LIBRARYS "${wxWidgets_LIBRARY_DIRS}/wx*")
message(${wxWidgets_LIBRARYS})
target_link_libraries(diff-pdf PRIVATE ${POPPLER_LIBRARIES} ${wxWidgets_LIBRARYS})
# Additional files to be distributed
set(EXTRA_DIST bootstrap gtk-zoom-in.xpm gtk-zoom-out.xpm README.md win32/fonts.conf win32/collect-dlls.sh)

# Custom target for Windows distribution
add_custom_target(windows-dist
    COMMAND ${CMAKE_COMMAND} -E remove_directory windist
    COMMAND ${CMAKE_COMMAND} -E make_directory windist
    COMMAND ${CMAKE_COMMAND} -E env bash ${CMAKE_SOURCE_DIR}/win32/collect-dlls.sh windist ued_doc_tools.exe
    COMMAND ${CMAKE_COMMAND} -E make_directory windist/fonts
    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_SOURCE_DIR}/win32/fonts.conf windist/fonts/
    COMMAND ${CMAKE_COMMAND} -E tar cf ued_doc_tools-win-${PROJECT_VERSION}.zip --format=zip -- ${CMAKE_BINARY_DIR}/windist
    COMMAND ${CMAKE_COMMAND} -E remove_directory windist
)