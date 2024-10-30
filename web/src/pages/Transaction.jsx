import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

export default function Transaction() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState({});

  useEffect(() => {
    fetch(`/api/core/get-transaction?id=${id}`)
      .then((res) => {
        if (res.ok) {
          return res.json();
        } else throw new Error("bad request");
      })
      .then((res) => {
        setData(res.transaction);
        // console.log(res.transaction);
      })
      .catch((err) => {
        //console.log(err);
        navigate("/404");
      });
  }, [id]);

  return <div>{id}</div>;
}
