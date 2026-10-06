import api from "./client";

export const registerStudent = async (data) => {
  const res = await api.post("/student/register", data);
  return res.data;
};

export const issueCertificate = async (data) => {
  const res = await api.post("/certificate/issue", data);
  return res.data;
};

export const getAllStudents = async () => {
  const res = await api.get("/university/allStudents");
  return res.data;
};