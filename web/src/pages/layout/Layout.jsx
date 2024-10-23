import { Outlet} from "react-router-dom";
import Navbar from "src/components/Navbar";


function Layout() {
  return (
    <>
      <Navbar />
      <br/>
        <Outlet />
    </>
  );
}

export default Layout;
