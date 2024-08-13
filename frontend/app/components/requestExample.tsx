"use client";
import React, { useState, useEffect, use } from "react";
import {
  Button,
  Modal,
  ModalHeader,
  Image,
  Divider,
  ModalBody,
  ModalFooter,
  Code,
  useDisclosure,
  ModalContent
} from "@nextui-org/react";
export default function RequestExample({modalOpen, onModalChange}: {modalOpen: boolean, onModalChange: () => void}) {

  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState("");

  // Clear the response when the modal is opened
  useEffect(() => {
    if (modalOpen) {
      setResponse("");
    }
  }
  , [modalOpen]);

  // Send a slow request to the backend
  const sendRequestSlow = async () => {
    setLoading(true);
    setResponse("");
    const res = await fetch(process.env.API_URL + "/api/delay");
    if (!res.ok) {
      setResponse("Error: " + res.status);
      setLoading(false);
      return;
    }
    const data = await res.json();
    
    setResponse(JSON.stringify(data, null, 2));
    setLoading(false);
  }

  // Send a fast request to the backend
  const sendRequestFast = async () => {
    setLoading(true);
    setResponse("");
    const res = await fetch(process.env.API_URL + "/api/health");
    if (!res.ok) {
      setResponse("Error: " + res.status);
      setLoading(false);
      return;
    }
    const data = await res.json();
    
    setResponse(JSON.stringify(data, null, 2));
    setLoading(false);
  }

  return (
    <Modal isOpen={modalOpen} onOpenChange={onModalChange} backdrop="blur">
      <ModalContent>
        <ModalHeader className="flex gap-3">
          <Image
            alt="nextui logo"
            height={40}
            radius="sm"
            src="https://avatars.githubusercontent.com/u/86160567?s=200&v=4"
            width={40}
          />
          <div className="flex flex-col">
            <p className="text-md">Example Request to Backend</p>
          </div>
        </ModalHeader>
        <Divider />
        <ModalBody>
          <p>Click the button below to send a request to the backend. The response will pop up below!</p>
          {response != "" && 
            <Code className="text-wrap">
              {response}
            </Code>
          }
        </ModalBody>
        <Divider />
        <ModalFooter>
        <Button
            isLoading={loading}
            onClick={() => sendRequestSlow()}
            color="secondary"
          >
            {loading ? "Loading..." : "Send Slow Request"}
          </Button>
          <Button
            isLoading={loading}
            onClick={() => sendRequestFast()}
            color="primary"
          >
            {loading ? "Loading..." : "Send Fast Request"}
          </Button>

        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}
