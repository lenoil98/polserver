/*
History
=======
2009/11/11 Turley:   Changed MAX_CONTAINER_ITEMS too highest possible value (3200)

Notes
=======

*/

#ifndef UCFG_H
#define UCFG_H

#define MAXBUFFER 2560

#define MAX_CONTAINER_ITEMS 3200 //0x3C packet maxsize 5+3200*20 ~= 0xFFFF
#define MAX_SLOTS 255

#define MAX_STACK_ITEMS		60000L
#define MAX_WEIGHT          65535L

#include "../../clib/maputil.h"
#include "../../clib/refptr.h"

#include "../module/fileaccess.h"

#include <boost/noncopyable.hpp>
#include <vector>
#include <map>
#include <string>

namespace Pol {
  namespace Module {
	class DataStoreFile;
  }
  namespace Core {
  class StoredConfigFile;
  typedef ref_ptr<StoredConfigFile> ConfigFileRef;

  typedef std::map<std::string, ConfigFileRef> CfgFiles;
  typedef std::vector<std::string> OldCfgFiles; // we've multiple older instances

  typedef std::map< std::string, Module::DataStoreFile*, Clib::ci_cmp_pred > DataStore;
  // used for Pol and RunEcl

  class ConfigurationBuffer : boost::noncopyable
  {
	public:
	  ConfigurationBuffer();
	  ~ConfigurationBuffer();

	  void deinialize();

	  CfgFiles cfgfiles;
	  OldCfgFiles oldcfgfiles;
	  DataStore datastore;
	  std::vector<Module::FileAccess> file_access_rules;
	private:
  };

  extern ConfigurationBuffer configurationbuffer;
  }
}

#endif
