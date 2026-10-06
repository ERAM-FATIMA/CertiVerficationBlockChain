import api from "./client";

export const verifyCertificate = async (formData) => {
  const res = await api.post(
    "/employer/verify-certificate",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return res.data;
};