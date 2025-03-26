import { useRef, useState } from 'react';
import { postItem } from '~/api';

interface Prop {
  onListingCompleted: () => void;
}

type FormDataType = {
  'item-name': string;
  'item-category': string;
  image: string | File;
};

export const Listing = ({ onListingCompleted }: Prop) => {
  const initialState = {
    'item-name': '',
    'item-category': '',
    image: '',
  };
  const [values, setValues] = useState<FormDataType>(initialState);

  const uploadImageRef = useRef<HTMLInputElement>(null);

  const onValueChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValues({
      ...values,
      [event.target.name]: event.target.value,
    });
  };
  const onFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValues({
      ...values,
      [event.target.name]: event.target.files![0],
    });
  };
  const onSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    // Validate field before submit
    const REQUIRED_FILEDS = ['name', 'image'];
    const missingFields = Object.entries(values)
      .filter(([, value]) => !value && REQUIRED_FILEDS.includes(value))
      .map(([key]) => key);

    if (missingFields.length) {
      alert(`Missing fields: ${missingFields.join(', ')}`);
      return;
    }

    // Submit the form
    postItem({
      name: values['item-name'],
      category: values['item-category'],
      image: values.image,
    })
      .then(() => {
        alert('Item listed successfully');
      })
      .catch((error) => {
        console.error('POST error:', error);
        alert('Failed to list this item');
      })
      .finally(() => {
        onListingCompleted();
        setValues(initialState);
        if (uploadImageRef.current) {
          uploadImageRef.current.value = '';
        }
      });
  };
  return (
    <div className="Listing">
      <form onSubmit={onSubmit}>
        <div>
          <input
            type="text"
            name="item-name"
            id="name"
            placeholder="name"
            autoComplete='on'
            onChange={onValueChange}
            required
            value={values['item-name']}
          />
          <input
            type="text"
            name="item-category"
            id="category"
            placeholder="category"
            autoComplete="on"
            onChange={onValueChange}
            value={values['item-category']}
          />
          <input
            type="file"
            name="image"
            id="image"
            onChange={onFileChange}
            required
            ref={uploadImageRef}
          />
          <button type="submit">List this item</button>
        </div>
      </form>
    </div>
  );
};
