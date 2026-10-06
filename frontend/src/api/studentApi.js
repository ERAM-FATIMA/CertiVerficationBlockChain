import api from "./client";

export const getCertificates = async () => {
  const res = await api.get("/student/viewCertificates");
  return res.data;
};
