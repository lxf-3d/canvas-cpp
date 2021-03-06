#include <tut/tut_console_reporter.hpp>
#include <tut/tut_main.hpp>

#include <iostream>

namespace tut
{
   test_runner_singleton runner;
}

class outbuf : public std::streambuf
{
   public:
      outbuf()
      {
         setp(0, 0);
      }

      virtual int_type overflow(int_type c = traits_type::eof())
      {
         return c;
      }
};

int main(int argc, const char* argv[])
{
   tut::console_reporter reporter;
   tut::runner.get().set_callback(&reporter);
   
   // Redirect std::cerr so we don't print anything while running tests
   outbuf ob;
   std::streambuf *sb = std::cerr.rdbuf(&ob);

   try
   {
      if(tut::tut_main(argc, argv))
      {
         std::cerr.rdbuf(sb);
         if(reporter.all_ok())
         {
            return 0;
         }
         else
         {
            std::cerr << "\nUnit test failed!" << std::endl;
         }
      }
   }
   catch(const tut::no_such_group &ex)
   {
      std::cerr << "No such group: " << ex.what() << std::endl;
   }
   catch(const tut::no_such_test &ex)
   {
      std::cerr << "No such test: " << ex.what() << std::endl;
   }
   catch(const tut::tut_error &ex)
   {
      std::cout << "General error: " << ex.what() << std::endl;
   }

   return 0;
}

