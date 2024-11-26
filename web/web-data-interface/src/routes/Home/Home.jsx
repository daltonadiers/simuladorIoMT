import React, { useState, useEffect } from "react";
import { MdEdit } from "react-icons/md";
import { FaRegTrashAlt } from "react-icons/fa";
import {
  getCollectedData,
  getUserName,
  inHouse,
  postData,
  putData,
  deleteData,
} from "../../components/api";
import { useAuth } from "../../components/AuthContext";
import DataTable from "react-data-table-component";
import { Container, Button, Modal, Form } from "react-bootstrap";
import "./Home.css";

const dadosDeSaude = new Map([
  [1, "Pressão arterial"],
  [2, "SPO2"],
  [3, "Temperatura Corporal"],
]);

const Home = () => {
  const [isEditing, setIsEditing] = useState(false);
  const [editRowId, setEditRowId] = useState(null);
  const [editRowInhouse, setEditRowInhouse] = useState(null);
  const [measurements, setMeasurements] = useState([]);
  const [user, setUser] = useState([]);
  const [filteredMeasurements, setFilteredMeasurements] = useState([]);
  const { token, clearToken } = useAuth();

  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    type: "",
    value1: "",
    value2: "",
  });

  const fetchMeasurements = async () => {
    if (token) {
      try {
        const data = await getCollectedData(token);
        const userResponse = await getUserName(token);

        if (data) {
          setMeasurements(data);
          setFilteredMeasurements(data);
        } else {
          console.error("Erro ao carregar os dados da API.");
        }

        if (userResponse) {
          setUser(userResponse);
        } else {
          console.error("Erro ao carregar os dados da API.");
        }
      } catch (error) {
        console.error("Erro ao buscar dados:", error);
      }
    }
  };

  useEffect(() => {
    fetchMeasurements();
  }, [token]);

  const handleLogout = () => {
    clearToken();
  };

  const handleEdit = (row) => {
    setIsEditing(true);
    setEditRowId(row.seq);
    setEditRowInhouse(row.inhouse);
    setFormData({
      type: String(row.type), // Convertendo para string para coincidir com o `value` do <select>
      value1: row.value1,
      value2: row.value2 || "",
    });
    setShowModal(true);
  };

  const handleDelete = async (row) => {
    if (window.confirm(`Deseja realmente excluir a medição?`)) {
      try {
        const result = await deleteData(token, row.seq);
        setFilteredMeasurements((prev) =>
          prev.filter((measurement) => measurement.seq !== row.seq)
        );
        alert("Item excluído com sucesso!");
      } catch (error) {
        alert("Erro ao excluir o item. Tente novamente mais tarde.");
        console.error(error);
      }
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();

    try {
      const updatedMeasurement = {
        userid: 0,
        type: parseInt(formData.type, 10),
        value1: parseFloat(formData.value1),
        value2: formData.type === "3" ? 0 : parseFloat(formData.value2),
        inhouse: editRowInhouse
      };

      const response = await putData(token, editRowId, updatedMeasurement);

      if (response && response.success) {
        setFilteredMeasurements((prev) =>
          prev.map((measurement) =>
            measurement.seq === editRowId
              ? { ...measurement, ...updatedMeasurement }
              : measurement
          )
        );
        setMeasurements((prev) =>
          prev.map((measurement) =>
            measurement.seq === editRowId
              ? { ...measurement, ...updatedMeasurement }
              : measurement
          )
        );

        alert("Medição atualizada com sucesso!");
        handleCloseModal();
      } else {
        throw new Error("Falha ao atualizar medição. Tente novamente.");
      }
    } catch (error) {
      console.error("Erro ao atualizar medição:", error);
      alert("Erro ao atualizar medição. Tente novamente.");
    }
  };

  const handleShowModal = () => setShowModal(true);

  const handleCloseModal = () => {
    setShowModal(false);
    setFormData({ type: "", value1: "", value2: "" });
    setIsEditing(false);
    setEditRowId(null);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    try {
      let house = false;
  
      try {
        house = await inHouse(user);
      } catch (error) {
        console.error("Erro ao verificar localização:", error);
      }
  
      const newMeasurement = {
        userid: 0,
        type: parseInt(formData.type, 10),
        value1: parseFloat(formData.value1),
        value2: formData.type === "3" ? 0 : parseFloat(formData.value2),
        inhouse: house,
      };
  
      const response = await postData(token, newMeasurement);
  
      if (response && response.success) {
        alert("Medição criada com sucesso!");
        handleCloseModal();
  
        await fetchMeasurements();
      } else {
        throw new Error("Falha ao criar medição. Tente novamente.");
      }
    } catch (error) {
      console.error("Erro ao criar medição:", error);
      alert("Erro ao criar medição. Tente novamente.");
    }
  };

  const columns = [
    {
      name: "Tipo",
      selector: (row) => dadosDeSaude.get(row.type) || "Tipo desconhecido",
      sortable: true,
    },
    {
      name: "Valor 1",
      selector: (row) => row.value1,
      sortable: true,
    },
    {
      name: "Valor 2",
      selector: (row) => row.value2,
      sortable: true,
    },
    {
      name: "Em Casa",
      selector: (row) => (row.inhouse ? "Sim" : "Não"),
      sortable: true,
    },
    {
      name: "Data/Hora",
      selector: (row) => {
        const utcDate = new Date(row.datetime + "Z");
        return new Intl.DateTimeFormat("pt-BR", {
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
          hour12: false,
          timeZone: "America/Sao_Paulo", 
        }).format(utcDate);
      },
      sortable: true,
    },
    {
      name: "Editar",
      cell: (row) => (
        <Button
          variant="warning"
          size="sm"
          onClick={() => handleEdit(row)}
          className="d-flex align-items-center"
        >
          <MdEdit className="me-1" /> {/* Ícone antes do texto */}
          Editar
        </Button>
      ),
      ignoreRowClick: true,
      allowOverflow: true,
      button: true,
    },
    {
      name: "Excluir",
      cell: (row) => (
        <Button variant="danger" size="sm" onClick={() => handleDelete(row)}>
          <FaRegTrashAlt className="me-1" />
          Excluir
        </Button>
      ),
      ignoreRowClick: true,
      allowOverflow: true,
      button: true,
    },
  ];

  return (
    <Container>
      <h1 className="my-4">Olá, {user.name}</h1>

      <Button variant="primary" onClick={handleShowModal} className="mb-4">
        Criar Nova Medição
      </Button>

      <DataTable
        title="Suas medições:"
        columns={columns}
        data={filteredMeasurements}
        pagination
        highlightOnHover
        striped
        dense
        fixedHeader
        className="custom-data-table"
      />
      <Button variant="danger" onClick={handleLogout} className="my-4">
        Sair
      </Button>

      <Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>
            {isEditing ? "Editar Medição" : "Criar Nova Medição"}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={isEditing ? handleUpdate : handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Tipo</Form.Label>
              <Form.Control
                as="select"
                name="type"
                value={formData.type}
                onChange={handleChange}
                required
              >
                <option value="">Selecione o tipo</option>
                {[...dadosDeSaude.entries()].map(([key, value]) => (
                  <option key={key} value={key}>
                    {value}
                  </option>
                ))}
              </Form.Control>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Valor 1</Form.Label>
              <Form.Control
                type="text"
                name="value1"
                value={formData.value1}
                onChange={handleChange}
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Valor 2</Form.Label>
              <Form.Control
                type="text"
                name="value2"
                value={formData.value2}
                onChange={handleChange}
                disabled={formData.type === "3"} // Desabilita se for "Temperatura Corporal"
              />
            </Form.Group>
            <Button variant="primary" type="submit">
              {isEditing ? "Salvar Alterações" : "Criar"}
            </Button>
          </Form>
        </Modal.Body>
      </Modal>
    </Container>
  );
};

export default Home;