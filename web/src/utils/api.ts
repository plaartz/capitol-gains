export const search = (
  pageNo = 1,
  pageSize = 100,
  orderBy: string | null = null,
  order: string | undefined = undefined
) => {
  return `api/core/search?pageNo=${
    pageNo > 0 ? pageNo : 1
  }&pageSize=${Math.max(Math.min(pageSize, 100), 1)}${
    orderBy
      ? `&orderBy=${orderBy}&order=${order == "ASC" ? "ASC" : "DESC"}`
      : ""
  }`;
};

export default search;
