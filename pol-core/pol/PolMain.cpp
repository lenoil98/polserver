#include "PolMain.h"

#include "../clib/Program/ProgramMain.h"
#include "pol.h"

namespace Pol
{
namespace Clib
{
using namespace std;

///////////////////////////////////////////////////////////////////////////////

PolMain::PolMain() : ProgramMain() {}
PolMain::~PolMain() {}
///////////////////////////////////////////////////////////////////////////////
void PolMain::showHelp()
{
  // no help available
}

int PolMain::main()
{
  // TODO: merge the following with all the other xmain* functions
  return Pol::xmain_outer( programArgsFind( "test" ), programArgsFind( "allow-executeprocess" ) );
}
}  // namespace Clib
}  // namespace Pol

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

int main( int argc, char* argv[] )
{
  Pol::Clib::PolMain* polMain = new Pol::Clib::PolMain();
  polMain->start( argc, argv );
}
